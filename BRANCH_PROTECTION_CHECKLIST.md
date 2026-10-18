# ✅ Branch Protection Setup Checklist

## Repository → Settings → Branches → Branch protection rules

### For `main` branch — REQUIRED SETTINGS:

- [ ] **Require pull request reviews before merging** — At least 1 approval
- [ ] **Require review from Code Owners** — ✅ ENABLED
- [ ] **Require status checks to pass before merging** — Select these checks:
  - [ ] CI / validate
  - [ ] CodeQL / Analyze (javascript-typescript)
  - [ ] CodeQL / Analyze (python)
  - [ ] Dependency Review / scan
  - [ ] Gitleaks Secret Scan / scan
- [ ] **Require branches to be up to date before merging** — ✅ ENABLED
- [ ] **Prevent direct pushes to `main`** — ✅ ENABLED
- [ ] **Do not allow bypassing the above** — ✅ ENABLED

## Code Security & Analysis — Settings → Security & analysis

- [ ] **Secret scanning** — Enabled ✅
- [ ] **Push protection** — Enabled ✅ (blocks commits containing known secrets)
- [ ] **Code scanning** — CodeQL enabled ✅

## Dependabot — Settings → Code security & analysis

- [ ] **Dependabot alerts** — Enabled ✅
- [ ] **Dependabot security updates** — Enabled ✅
