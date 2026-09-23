Here’s your complete, ready-to-save **FIX_FAIL_JOB.md** troubleshooting guide — tailored exactly to your workflow issues and folder structure:

---

# 🔧 FIX_FAIL_JOB.md
## Troubleshooting Guide — Failing GitHub Actions Workflows

**Last Updated:** 2026-09-23  
**Repo:** `crystalcastleX`  
**Owner:** ZyntroAI  

---

## 📋 Overview
This document resolves common CI failures — especially `update-readme.yml` — caused by:
- Path conflicts (file vs directory)
- Git permission / push failures
- Node.js version deprecation warnings
- Folder restructure migration issues

---

## ❌ Error Reference Table

| Error Message | Root Cause | Priority | Fix Section |
|---|---|---|---|
| `The process '/usr/bin/git' failed with exit code 128` | No write permission; shallow clone; or nothing to push | 🔴 High | §3.1 |
| `cannot create directory at 'docs/knowledge/...'` | A **file** named `docs/knowledge` blocks the **directory** of the same name | 🔴 High | §3.2 |
| `Node.js 20 is deprecated` | Using `actions/checkout@v4` → upgrade to `v5` | 🟡 Medium | §3.3 |
| `fatal: not a git repository` | Missing `fetch-depth` or wrong checkout ref | 🟡 Medium | §3.4 |
| `python: can't open file 'scripts/update_readme.py'` | Path moved after folder restructure | 🔴 High | §3.5 |

---

## 🚨 1. Immediate Emergency Fix
Run these commands **locally** on `main` branch to clear the most common blockers:

```bash
# 1. Sync latest
git checkout main
git pull origin main

# 2. Diagnose path conflict
ls -la docs/

# 3. Fix file/directory name collision
if [ -f "docs/knowledge" ]; then
  mv docs/knowledge docs/knowledge.bak.md
  echo "✅ Renamed conflicting file → docs/knowledge.bak.md"
fi

# 4. Ensure directory exists
mkdir -p docs/knowledge

# 5. Commit resolution
git add docs/
git commit -m "fix: resolve docs/knowledge file-dir path conflict"
git push origin main

# 6. Verify script location
ls -la scripts/update_readme.py
# If missing → move to new location per folder restructure
```

---

## 🔍 2. Diagnosis Steps
When a job fails:

### 2.1 Check Permissions
- Go to failed job → **Review permissions** at top
- Verify workflow file has:
  ```yaml
  permissions:
    contents: write
  ```
- If missing → workflow can **read only** → push fails with `exit 128`

### 2.2 Check Paths
- Look for `cannot create directory` → file exists where dir needed
- Check folder restructure status:
  - `frontend/` — client assets
  - `backend/` — server code
  - `development/` — docs/guides *(formerly `docs/`)*
- Update paths in workflows accordingly

### 2.3 Check Action Versions
- ✅ `actions/checkout@v5` — Node 24 compatible
- ✅ `actions/setup-python@v5` — latest stable
- ✅ `actions/upload-artifact@v4` — current

---

## ✅ 3. Resolutions

### 3.1 Git Push Failed — Exit Code 128
**Fix:**
```yaml
permissions:
  contents: write  # Required for push

steps:
  - uses: actions/checkout@v5
    with:
      fetch-depth: 0  # Full history
      token: ${{ secrets.GITHUB_TOKEN }}
```

**Commit logic must be explicit:**
```bash
git add .
if git diff --staged --quiet; then
  echo "✅ No changes — skipping commit"
  exit 0
fi
git commit -m "docs: auto-update"
git push origin main
```

### 3.2 Path Conflict — File vs Directory
**Root Cause:** Previous commit created a **file** at `docs/knowledge` → workflow cannot create **directory** with same name.

**Workflow Auto-Fix Step:**
```yaml
- name: 🧹 Resolve path conflicts
  run: |
    if [ -f "docs/knowledge" ]; then
      echo "⚠️ Renaming file → docs/knowledge.md"
      mv docs/knowledge docs/knowledge.md
    fi
    mkdir -p docs/knowledge
```

### 3.3 Node.js 20 Deprecation Warning
**Fix:** Upgrade all references:
| Old | New |
|---|---|
| `actions/checkout@v4` | `actions/checkout@v5` |
| `actions/setup-node@v4` | `actions/setup-node@v4` *(still OK; add env override)* |

**Suppress globally:**
```yaml
env:
  FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true
```

### 3.4 Folder Restructure — Path Updates
After migration completes:
| Old Path | New Path |
|---|---|
| `docs/knowledge/**` | `development/docs/knowledge/**` |
| `scripts/` | `development/scripts/` or repo root |
| `README.md` | Repo root — unchanged |

**Update workflow triggers:**
```yaml
paths:
  - 'development/docs/knowledge/**'
  - 'development/scripts/update_readme.py'
```

### 3.5 Python Script Not Found
**After restructure**, verify script location and update run step:
```yaml
- name: 🚀 Run README sync
  run: python development/scripts/update_readme.py
```

---

## 📂 4. Reference — Known Working `update-readme.yml`
```yaml
name: 📝 Update README from docs/knowledge

on:
  push:
    branches: [ main ]
    paths:
      - 'docs/knowledge/**'
      - 'scripts/update_readme.py'
  workflow_dispatch:
  schedule:
    - cron: '0 0 * * *'

env:
  FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true

permissions:
  contents: write

jobs:
  update-readme:
    runs-on: ubuntu-latest
    timeout-minutes: 10

    steps:
      - name: 📥 Checkout
        uses: actions/checkout@v5
        with:
          fetch-depth: 0
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: 🧹 Fix path conflict
        run: |
          [ -f "docs/knowledge" ] && mv docs/knowledge docs/knowledge.md
          mkdir -p docs/knowledge

      - name: 🐍 Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: 📦 Install deps
        run: pip install pyyaml

      - name: 🚀 Run sync
        run: python scripts/update_readme.py

      - name: ✍️ Commit & Push
        run: |
          git config --global user.name "github-actions[bot]"
          git config --global user.email "github-actions[bot]@users.noreply.github.com"
          git add README.md
          git diff --staged --quiet && exit 0
          git commit -m "docs: auto-sync knowledge → README"
          git push origin main
```

---

## 🧯 Prevention Checklist
- [ ] All workflows use `checkout@v5` or higher
- [ ] `permissions: contents: write` set on all push-enabled jobs
- [ ] Paths reviewed & updated after folder restructure
- [ ] No duplicate names (file vs directory)
- [ ] Scheduled runs verified active post-migration
- [ ] `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true` added globally

---

## 📞 Escalation
If issues persist:
1. Enable **debug logging** in failed job → rerun
2. Capture full error + job link
3. Check `.github/workflows/` for syntax via [Actions Lint](https://actionlint.net/)
4. Confirm branch protection rules aren't blocking `github-actions[bot]`

---

## ✍️ Changelog
| Date | Change | By |
|---|---|---|
| 2026-09-23 | Initial version — addresses `exit 128`, path conflicts, Node deprecation | ZyntroAI |

---

Save this file as **`.github/FIX_FAIL_JOB.md`** in your repository root.
