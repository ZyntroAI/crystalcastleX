📝 CHANGELOG — CrystalCastle X
 
Repo:  zyntromedia/crystalcastleX  | Standard: Keep a Changelog + SemVer | Last Updated: 2026-09-26
 
 
 
[Unreleased] — 2026-09-26 🔧 CI Hygiene

✨ Added

- `archive/workflows/ARCHIVE-MANIFEST.md` — records all 38 moved files with their blob SHAs, so any archived file can be located or restored by hash.

🧹 Changed

- Archived the inert top-level `workflows/` tree to `archive/workflows/` (38 files). GitHub Actions executes a workflow **only** at `.github/workflows/`, so that tree was dead weight that had drifted out of sync with live CI and collided on filename. Nothing under `.github/workflows/` was touched — the directory's tree hash is byte-identical (`1b17fa20`) across `main` and this branch.
- Repaired 2 filenames exceeding the 255-byte `NAME_MAX` limit — their bytes are preserved under deterministic names recorded in the manifest.

🐛 Fixed

- `consolidate-workflows.sh` matched **zero files silently** after the archive move (it read the now-gone `workflows/` path) and ended in a literal `git push origin <main>` placeholder that fails verbatim. Rewritten against `archive/workflows/`, dry-run by default, with a collision guard so a move cannot shadow a live workflow.
- `__tests__/workflows/test-yml.test.js` read `workflows/test.yml`, a file that **never existed** in this repository — verified absent from `main` and from all fetched history. `beforeAll` threw ENOENT on every run. Repointed at `.github/workflows/test-and-coverage.yml`; assertions verified 12/12 against the real file.
- Updated 6 stale `workflows/...` path references across `RELEASE_NOTES.md`, `.github/RELEASE_NOTES.md`, `Backend/README.md` and `.template-docs/Recommended Architecture`.

📌 Known Issues

- ~678 paths remain uncheckoutable due to over-`NAME_MAX` filenames (e.g. `docs/knowledge/howtotos.md` with document content pasted into the filename). Tracked separately; a normal `git checkout` still fails.
- `RELEASE_NOTES.md` references `workflows/Onboarding.md`, which does not exist anywhere in the repository. Left unrepaired rather than guessed at.
- `doc/index.md` status badges point at `1napz/crystalcastle` — wrong repository. Pre-existing and unrelated.

[1.0.0] — 2026-09-04 🚀 MAJOR RELEASE
 
Theme: Agentic DevSecOps + Obsidian Vault Full Integration
 
✨ Added
 
- Core Platform: Full GitLab 19.3 Agentic DevSecOps Pipeline (Plan → Code → Test → Deploy → Secure)
- Obsidian Vault: Complete DevSecOps structure + Local REST API (127.0.0.1:27124) with HTTPS/Bearer Auth
- Traceability System: Unique  trace_id  ( tr_<random> ) generator + standardized Thread/Deployment Template
- Automation: Templater scripts (ID/Date auto-fill) + Dataview Overview Dashboard ( Traces/Overview.md )
- Security Layer: SAST/SCA/Secret scanning + Dynamic/Policy checks + immutable artifact provenance
- CI/CD: Unified GitHub/GitLab workflows, smart caching, matrix builds, auto-rollback
- Documentation: Bilingual (EN/TH) README + API examples + setup guide + folder index
 
🔄 Changed
 
- Vault Structure: Reorganized →  Vault/Core | Config | Pipelines | Traces | Templates | Scripts 
- API: Upgraded REST API to v1.4 → strict TLS + token security
- Performance: Pipeline optimization → ~20x faster execution
- Config: Standardized environment + timezone (+07:00)
 
🐛 Fixed
 
- Resolved local  invalid link  vault errors
- Fixed Templater date/timezone handling
- Corrected permission/concurrency limits
 
🛡️ Security
 
- Secret detection + GitGuardian integration
- OPA compliance policies + full audit trail
- API restricted to localhost + short-lived tokens
 
 
 
[0.9.5] — 2026-09-01
 
✨ Added
 
- Initial Obsidian Vault base structure
- Trace/Thread ID system prototype
- Basic REST API connection
 
🔄 Changed
 
- Refined folder hierarchy
 
 
 
[0.8.0] — 2026-08-25
 
✨ Added
 
- GitLab CI/CD foundation
- Core security scanning setup
- Base README/license
 
 
 
📌 Notes
 
- Format: Semantic Versioning ( MAJOR.MINOR.PATCH )
- Status: ✅ Production Ready
- Location:  https://github.com/zyntromedia/crystalcastleX/blob/main/CHANGELOG.md 
 
 
 
📋 Full Ready-to-Paste Block
 
markdown
  
# Changelog — CrystalCastle X
All notable changes to this project will be documented here.
Format: [SemVer] — Date | Keep a Changelog Standard

## [1.0.0] — 2026-09-04
### Added
- Full Agentic DevSecOps Pipeline (GitLab 19.3)
- Obsidian DevSecOps Vault + Local REST API (:27124)
- Trace ID (`tr_*`) + Thread/Deployment Template
- Templater auto-gen scripts + Dataview Overview
- End-to-end Security: SAST/SCA/Secret/Dynamic/Policy
- Bilingual Docs + Unified CI/CD Workflows

### Changed
- Reorganized vault structure
- API upgraded: HTTPS + Token Auth
- Pipeline performance improved (~20x)

### Fixed
- Local link resolution errors
- Date/timezone consistency

### Security
- Secret detection + Provenance + Audit Logs
- Local-only API + Least Privilege

## [0.9.5] — 2026-09-01
- Initial Vault + Trace system

## [0.8.0] — 2026-08-25
- GitLab CI/CD base + Security setup
 
 
