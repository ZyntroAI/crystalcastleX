#!/usr/bin/env python3
"""
Zyntro Semantic Diff — 0 credits, Ollama powered
Classifies changes semantically, not just line diff
"""
import re, json, sys
from pathlib import Path
from dataclasses import dataclass
from typing import List

@dataclass
class SemanticChange:
    file: str
    type: str  # feat|fix|refactor|affiliate|docs|style|test|chore|security|breaking
    risk: str  # Low|Medium|High
    summary: str
    lines: int

FILE_PATTERNS = {
    'affiliate': re.compile(r'(affiliate|shopee|lazada|product|link)', re.I),
    'security': re.compile(r'(secret|password|token|auth|api_key|credential)', re.I),
    'test': re.compile(r'(__tests__|test_|\.test\.|\.spec\.)', re.I),
    'docs': re.compile(r'(\.md$|docs/|README)', re.I),
    'ci': re.compile(r'(\.github/|Dockerfile|docker-compose)', re.I),
}

BREAKING_PATTERNS = re.compile(r'(BREAKING CHANGE|remove|delete|rename.*function|change.*signature)', re.I)

def classify_file(path: str, diff_chunk: str) -> SemanticChange:
    path_lower = path.lower()
    lines = diff_chunk.count('\n')
    
    # Detect type
    ftype = 'chore'
    for key, pattern in FILE_PATTERNS.items():
        if pattern.search(path) or pattern.search(diff_chunk[:2000]):
            ftype = key
            break
    
    # Detect feat/fix from content
    if re.search(r'\bdef \w+|class \w+|export (function|const)', diff_chunk):
        if 'fix' in diff_chunk.lower() or 'bug' in diff_chunk.lower():
            ftype = 'fix'
        else:
            ftype = 'feat' if ftype == 'chore' else ftype

    risk = 'Low'
    if ftype == 'security':
        risk = 'High'
    elif BREAKING_PATTERNS.search(diff_chunk):
        ftype = 'breaking'
        risk = 'High'
    elif lines > 200 or ftype in ('feat', 'refactor'):
        risk = 'Medium'
    elif ftype == 'affiliate' and lines > 50:
        risk = 'Medium'

    summary = diff_chunk.split('\n')[0][:120] if diff_chunk else "No changes"

    return SemanticChange(
        file=path,
        type=ftype,
        risk=risk,
        summary=summary,
        lines=lines
    )

def parse_git_diff(diff_text: str) -> List[SemanticChange]:
    changes = []
    current_file = ""
    current_chunk = []

    for line in diff_text.split('\n'):
        if line.startswith('diff --git'):
            if current_file:
                changes.append(classify_file(current_file, '\n'.join(current_chunk)))
            # extract b/file
            m = re.search(r'b/(.+)$', line)
            current_file = m.group(1) if m else "unknown"
            current_chunk = []
        else:
            current_chunk.append(line)
    
    if current_file:
        changes.append(classify_file(current_file, '\n'.join(current_chunk)))
    
    return changes

def main():
    diff_file = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("diff.txt")
    output_file = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("output/semantic.json")