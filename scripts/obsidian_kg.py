#!/usr/bin/env python3
"""
🗂️ Obsidian Knowledge Graph Utilities
Validates links, generates backlinks, updates tags,
exports graph data, and enforces CrystalCastleX standards.

Usage:
    python scripts/obsidian_kg.py --scan ./docs
    python scripts/obsidian_kg.py --backlinks ./docs
    python scripts/obsidian_kg.py --export-graph ./docs graph.json
    python scripts/obsidian_kg.py --fix-headers ./docs
"""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

# ──────────────────────────────────────────────
# Constants & Patterns
# ──────────────────────────────────────────────
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(#[^\]|]+)?\|?([^\]]*)]]")
MARKDOWN_LINK_RE = re.compile(r"\[([^]]+)\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)
TAG_RE = re.compile(r"(?<!\w)#([\w/-]+)")
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
ALIAS_RE = re.compile(r"^aliases:\s*(.+)$", re.MULTILINE)
TITLE_RE = re.compile(r"^title:\s*(.+)$", re.MULTILINE)

# CrystalCastleX Standards
REQUIRED_FRONTMATTER_FIELDS = ["title", "date", "tags"]
STANDARD_FOLDERS = {
    "00-Inbox",
    "01-Journal",
    "02-Concepts",
    "03-Resources",
    "04-Areas",
    "05-Projects",
    "06-Archive",
    "99-System",
}

@dataclass
class Note:
    path: Path
    title: str
    aliases: Set[str] = field(default_factory=set)
    tags: Set[str] = field(default_factory=set)
    links: Set[str] = field(default_factory=set)
    backlinks: Set[str] = field(default_factory=set)
    frontmatter: Dict[str, Any] = field(default_factory=dict)
    modified: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    errors: List[str] = field(default_factory=list)

    @property
    def relative_path(self) -> str:
        return str(self.path.parent)

    @property
    def filename(self) -> str:
        return self.path.stem


# ──────────────────────────────────────────────
# File Parser
# ──────────────────────────────────────────────
class NoteParser:
    def __init__(self, vault_path: Path):
        self.vault_path = vault_path.resolve()
        self.notes: Dict[str, Note] = {}
        self._alias_map: Dict[str, str] = {}  # alias → canonical path

    def parse_note(self, file_path: Path) -> Note:
        """Parse a single markdown note"""
        text = file_path.read_text(encoding="utf-8")
        rel_path = file_path.relative_to(self.vault_path)
        modified = datetime.fromtimestamp(file_path.stat().st_mtime, tz=timezone.utc)

        # Parse frontmatter
        frontmatter = self._parse_frontmatter(text)
        title = frontmatter.get("title", file_path.stem)
        aliases = self._parse_aliases(frontmatter)
        tags = self._parse_tags(text, frontmatter)
        links = self._parse_links(text, file_path.parent)

        note = Note(
            path=rel_path,
            title=title,
            aliases=aliases,
            tags=tags,
            links=links,
            frontmatter=frontmatter,
            modified=modified,
        )

        # Validate
        self._validate_note(note, text)
        return note

    def _parse_frontmatter(self, text: str) -> Dict[str, Any]:
        match = FRONTMATTER_RE.match(text)
        if not match:
            return {}
        try:
            import yaml
            fm_text = match.group(1)
            return yaml.safe_load(fm_text) or {}
        except Exception:
            return {}

    def _parse_aliases(self, fm: Dict[str, Any]) -> Set[str]:
        aliases_raw = fm.get("aliases", [])
        if isinstance(aliases_raw, str):
            aliases_raw = [a.strip() for a in aliases_raw.split(",") if a.strip()]
        return set(aliases_raw)

    def _parse_tags(self, text: str, fm: Dict[str, Any]) -> Set[str]:
        tags = set()
        # Frontmatter tags
        fm_tags = fm.get("tags", [])
        if isinstance(fm_tags, str):
            fm_tags = [t.strip() for t in fm_tags.split(",") if t.strip()]
        for t in fm_tags:
            tags.add(t.lstrip("#"))
        # Inline #tags
        for match in TAG_RE.finditer(text):
            tags.add(match.group(1))
        return tags

    def _parse_links(self, text: str, source_dir: Path) -> Set[str]:
        links = set()
        # Wiki-style links [[Note]] or [[Note#Section|Display]]
        for match in WIKILINK_RE.finditer(text):
            target = match.group(1).strip()
            if target and not target.startswith("http"):
                links.add(target)
        # Standard markdown links [text](file.md)
        for match in MARKDOWN_LINK_RE.finditer(text):
            url = match.group(2)
            if url.endswith(".md") and not url.startswith("http"):
                links.add(url.replace(".md", ""))
        return links

    def _validate_note(self, note: Note, text: str) -> None:
        """Check CrystalCastleX standards"""
        # Frontmatter check
        missing = [f for f in REQUIRED_FRONTMATTER_FIELDS if f not in note.frontmatter]
        if missing:
            note.errors.append(f"Missing frontmatter fields: {', '.join(missing)}")
        # Title matches filename
        if note.title != note.path.stem:
            note.errors.append(f"Title mismatch: title='{note.title}' vs filename='{note.path.stem}'")
        # No empty headings
        for match in HEADING_RE.finditer(text):
            heading_text = match.group(2).strip()
            if not heading_text:
                note.errors.append("Empty heading found")
        # Tags should not have spaces
        for tag in note.tags:
            if " " in tag:
                note.errors.append(f"Tag has spaces: #{tag} — use hyphens")

    def scan_vault(self) -> Dict[str, Note]:
        """Scan entire vault for markdown files"""
        for md_file in self.vault_path.rglob("*.md"):
            if ".trash" not in str(md_file) and ".obsidian" not in str(md_file):
                note = self.parse_note(md_file)
                path_key = str(note.path)
                self.notes[path_key] = note
                # Register aliases
                for alias in note.aliases:
                    if alias not in self._alias_map:
                        self._alias_map[alias] = path_key
        return self.notes

    def resolve_backlinks(self) -> None:
        """Populate backlinks for all notes"""
        # Build title/alias → path index
        name_index: Dict[str, str] = {}
        for path, note in self.notes.items():
            name_index[note.filename] = path
            name_index[note.title] = path
            for alias in note.aliases:
                name_index[alias] = path

        # Resolve each link
        for source_path, note in self.notes.items():
            for link in note.links:
                target_path = name_index.get(link) or self._resolve_path(link, source_path)
                if target_path and target_path in self.notes:
                    self.notes[target_path].backlinks.add(source_path)

    def _resolve_path(self, link: str, source_path: str) -> Optional[str]:
        """Try to resolve relative paths"""
        source_dir = Path(source_path).parent
        for candidate in [
            source_dir / f"{link}.md",
            self.vault_path / f"{link}.md",
            *self.vault_path.rglob(f"{link}.md"),
        ]:
            if candidate.exists():
                return str(candidate.relative_to(self.vault_path))
        return None


# ──────────────────────────────────────────────
# Graph Exporter
# ──────────────────────────────────────────────
class GraphExporter:
    def __init__(self, notes: Dict[str, Note]):
        self.notes = notes

    def to_json(self, output_path: Path) -> None:
        """Export full graph to JSON"""
        nodes = []
        edges = []
        seen_edges: Set[Tuple[str, str]] = set()

        for path, note in self.notes.items():
            nodes.append({
                "id": path,
                "label": note.title,
                "aliases": list(note.aliases),
                "tags": list(note.tags),
                "path": path,
                "folder": note.relative_path,
                "modified": note.modified.isoformat(),
                "backlink_count": len(note.backlinks),
                "link_count": len(note.links),
            })
            for target in note.links:
                edge = (path, target)
                if edge not in seen_edges:
                    edges.append({"source": path, "target": target})
                    seen_edges.add(edge)

        graph = {
            "version": "1.0",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "stats": {
                "node_count": len(nodes),
                "edge_count": len(edges),
                "orphan_count": sum(1 for n in nodes if n["backlink_count"] == 0 and n["link_count"] == 0),
            },
            "nodes": nodes,
            "edges": edges,
        }

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(graph, f, indent=2, ensure_ascii=False)
        print(f"📊 Graph exported: {output_path}")

    def to_csv(self, nodes_path: Path, edges_path: Path) -> None:
        """Export as two CSV files for analysis"""
        import csv

        with open(nodes_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "label", "tags", "path", "backlink_count"])
            writer.writeheader()
            for path, note in self.notes.items():
                writer.writerow({
                    "id": path,
                    "label": note.title,
                    "tags": ", ".join(note.tags),
                    "path": path,
                    "backlink_count": len(note.backlinks),
                })

        with open(edges_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["source", "target"])
            writer.writeheader()
            seen = set()
            for path, note in self.notes.items():
                for target in note.links:
                    if (path, target) not in seen:
                        writer.writerow({"source": path, "target": target})
                        seen.add((path, target))

        print(f"📄 Nodes: {nodes_path}")
        print(f"📄 Edges: {edges_path}")


# ──────────────────────────────────────────────
# Frontmatter & Header Fixer
# ──────────────────────────────────────────────
class NoteFixer:
    def __init__(self, vault_path: Path):
        self.vault_path = vault_path.resolve()

    def ensure_frontmatter(self, file_path: Path) -> bool:
        """Ensure note has standard CrystalCastleX frontmatter"""
        text = file_path.read_text(encoding="utf-8")
        today = datetime.now().strftime("%Y-%m-%d")
        title = file_path.stem

        if FRONTMATTER_RE.match(text):
            return False  # Already has frontmatter

        fm = f"""---
title: {title}
date: {today}
tags: []
---

"""
        file_path.write_text(fm + text, encoding="utf-8")
        print(f"✅ Added frontmatter: {file_path.name}")
        return True

    def normalize_headers(self, file_path: Path) -> bool:
        """Ensure H1 matches title, fix header hierarchy"""
        text = file_path.read_text(encoding="utf-8")
        title = file_path.stem

        # Check for existing H1
        h1_match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
        if not h1_match:
            text = f"# {title}\n\n{text}"
            file_path.write_text(text, encoding="utf-8")
            print(f"✅ Added H1: {file_path.name}")
            return True
        return False


# ──────────────────────────────────────────────
# Main CLI
# ──────────────────────────────────────────────
def cmd_scan(args):
    """Scan vault and report issues"""
    vault = Path(args.vault).resolve()
    parser = NoteParser(vault)
    notes = parser.scan_vault()
    parser.resolve_backlinks()

    print(f"\n📋 Scan Results — {len(notes)} notes found\n")

    total_errors = 0
    for path, note in sorted(notes.items()):
        if note.errors:
            total_errors += len(note.errors)
            print(f"⚠️  {path}")
            for err in note.errors:
                print(f"   • {err}")
        elif args.verbose:
            print(f"✅ {path} — #{', #'.join(note.tags or ['untagged'])} — {len(note.links)} links, {len(note.backlinks)} backlinks")

    orphans = [p for p, n in notes.items() if not n.backlinks and not n.links]
    if orphans:
        print(f"\n📌 Orphan notes (no links): {len(orphans)}")
        if args.verbose:
            for o in orphans:
                print(f"   • {o}")

    print(f"\n📊 Summary: {len(notes)} notes | {total_errors} issues | {len(orphans)} orphans")


def cmd_backlinks(args):
    """Show backlinks for a specific note"""
    vault = Path(args.vault).resolve()
    parser = NoteParser(vault)
    notes = parser.scan_vault()
    parser.resolve_backlinks()

    target_path = None
    for p in notes:
        if Path(p).stem == args.note_name or p == args.note_name:
            target_path = p
            break

    if not target_path:
        print(f"❌ Note not found: {args.note_name}")
        return

    note = notes[target_path]
    print(f"\n🔗 Backlinks for: {note.title}\n")
    if note.backlinks:
        for bl in sorted(note.backlinks):
            print(f"   • {bl}")
    else:
        print("   No backlinks yet.")
    print(f"\nTotal: {len(note.backlinks)} backlinks")


def cmd_export(args):
    """Export graph to JSON/CSV"""
    vault = Path(args.vault).resolve()
    parser = NoteParser(vault)
    notes = parser.scan_vault()
    parser.resolve_backlinks()
    exporter = GraphExporter(notes)

    out_path = Path(args.output)
    if args.format == "json" or out_path.suffix == ".json":
        exporter.to_json(out_path)
    elif args.format == "csv" or out_path.suffix == ".csv":
        stem = out_path.with_suffix("")
        exporter.to_csv(Path(f"{stem}_nodes.csv"), Path(f"{stem}_edges.csv"))
    else:
        print("❌ Unsupported format. Use .json or .csv")


def cmd_fix(args):
    """Fix frontmatter and headers"""
    vault = Path(args.vault).resolve()
    fixer = NoteFixer(vault)
    count = 0

    for md_file in vault.rglob("*.md"):
        if ".trash" in str(md_file) or ".obsidian" in str(md_file):
            continue
        if fixer.ensure_frontmatter(md_file):
            count += 1
        if args.fix_headers and fixer.normalize_headers(md_file):
            count += 1

    print(f"\n✅ Fixed {count} files")


def main():
    parser = argparse.ArgumentParser(
        description="🗂️ Obsidian Knowledge Graph Utilities — CrystalCastleX",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/obsidian_kg.py --scan ./docs
  python scripts/obsidian_kg.py --backlinks ./docs "Project Alpha"
  python scripts/obsidian_kg.py --export ./docs graph.json
  python scripts/obsidian_kg.py --fix ./docs --fix-headers
        """,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Scan
    scan_parser = subparsers.add_parser("scan", help="Scan vault for issues")
    scan_parser.add_argument("vault", help="Path to vault root")
    scan_parser.add_argument("-v", "--verbose", action="store_true")

    # Backlinks
    bl_parser = subparsers.add_parser("backlinks", help="Show backlinks for a note")
    bl_parser.add_argument("vault", help="Path to vault root")
    bl_parser.add_argument("note_name", help="Note filename or title")

    # Export
    exp_parser = subparsers.add_parser("export", help="Export graph to JSON/CSV")
    exp_parser.add_argument("vault", help="Path to vault root")
    exp_parser.add_argument("output", help="Output file path")
    exp_parser.add_argument("--format", choices=["json", "csv"], default="json")

    # Fix
    fix_parser = subparsers.add_parser("fix", help="Auto-fix frontmatter & headers")
    fix_parser.add_argument("vault", help="Path to vault root")
    fix_parser.add_argument("--fix-headers", action="store_true", help="Also fix H1 headers")

    # Shortcuts
    parser.add_argument("--scan", dest="shortcut_scan", help=argparse.SUPPRESS, nargs=2)
    parser.add_argument("--backlinks", dest="shortcut_bl", help=argparse.SUPPRESS, nargs=3)
    parser.add_argument("--export", dest="shortcut_exp", help=argparse.SUPPRESS, nargs="+")
    parser.add_argument("--fix", dest="shortcut_fix", help=argparse.SUPPRESS, nargs="+")

    args = parser.parse_args()

    # Handle shortcut flags
    if args.shortcut_scan:
        args.command = "scan"
        args.vault = args.shortcut_scan[0]
        args.verbose = False
    elif args.shortcut_bl:
        args.command = "backlinks"
        args.vault = args.shortcut_bl[0]
        args.note_name = args.shortcut_bl[1]
    elif args.shortcut_exp:
        args.command = "export"
        args.vault = args.shortcut_exp[0]
        args.output = args.shortcut_exp[1]
        args.format = "json"
    elif args.shortcut_fix:
        args.command = "fix"
        args.vault = args.shortcut_fix[0]
        args.fix_headers = "--fix-headers" in args.shortcut_fix

    # Dispatch
    if args.command == "scan":
        cmd_scan(args)
    elif args.command == "backlinks":
        cmd_backlinks(args)
    elif args.command == "export":
        cmd_export(args)
    elif args.command == "fix":
        cmd_fix(args)


if __name__ == "__main__":
    main()
