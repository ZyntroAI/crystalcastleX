# REMARK_NOTES.md

**Task:** UPD-20260914-0529 — Full repository compare & update
**Repo:** `ZyntroAI/crystalcastleX`
**Date:** 2026-09-14

Files that were **deliberately not modified** because an update would be risky, breaking, or
out of scope. None of these block the update — every one is skipped with the project running
as before. Each entry records the exact path, the issue, the current state, the update risk,
and the goal for a later release.

**Count: 22 entries across 6 categories.** Priority: 🔴 do next · 🟠 soon · 🟡 scheduled.

---

## Category A — Committed credentials (🔴 HIGHEST PRIORITY)

### A1. `.env.local` (tracked in git)
- **Issue:** Contains live-looking secrets committed to the repository: `OPEN_AI_KEY`,
  `OPENROUTER_API_KEY`, `GH_KEY` (`ghp_…` GitHub PAT), `CLOUDFLARE_API_TOKEN`,
  `COPILOT_METRIC_TOKEN` (`ghp_…`), `Vercel_Client_secret`, `AI_GATEWAY_API_KEY`, a Supabase
  URL/anon key, and a ClickUp token.
- **Current state:** still present in the working tree; **no longer tracked** after this
  update (`git rm --cached`), and `.gitignore` now excludes `.env.local` explicitly.
- **Update risk:** HIGH — untracking removes it from future commits but does **not** erase it
  from git history.
- **LATER GOAL:** **Rotate every credential in this file now** — they must be treated as
  compromised. Then purge history (`git filter-repo --path .env.local --invert-paths` or BFG)
  and force-push, or accept the exposure if the repo is private and the tokens are dead.

### A2. `.env` (tracked in git)
- **Issue:** Contains a placeholder (`ANTHROPIC_API_KEY="your-api-key-here"`), not a real
  secret — but `.env` should never be tracked regardless, and it is not a valid `.env` (it is
  an `export` shell line, not KEY=VALUE).
- **Current state:** working but wrong format; **no longer tracked** after this update.
- **Update risk:** LOW (placeholder only).
- **LATER GOAL:** delete the file entirely; `.env.example` is the correct template.

### A3. `src/api/flask_pdf2htmlEX_drive/service_account.json` (tracked in git)
- **Issue:** A Google Cloud **service-account key file**. If populated, this is a full GCP
  credential; `.gitignore` already lists `service-account.json` but this variant slipped
  through.
- **Current state:** NOT modified (content not inspected — the file may be a placeholder, but
  it must be assumed sensitive).
- **Update risk:** HIGH — do not touch without the user confirming whether it is real.
- **LATER GOAL:** confirm the key is revoked/rotated, untrack it, and add
  `**/service_account.json` to `.gitignore`.

---

## Category B — Unresolvable / non-existent actions (🟠)

These refs could not be SHA-pinned because the target does not resolve — the referenced
repository or tag does not exist. They were **left exactly as they are**; pinning them would
require inventing a SHA, which is worse than an unpinned ref.

### B1. `.github/workflows/notify.yml` → `some/notify-action@v1`
- **Issue:** `some/notify-action` is a placeholder namespace — no such public action exists.
- **Current state:** the step will fail if it runs; workflow is otherwise intact.
- **Update risk:** HIGH / BREAKING (removing it changes behaviour the author may rely on).
- **LATER GOAL:** replace with a real notifier (`slackapi/slack-github-action` or
  `appleboy/telegram-action`) in v1.5.x.

### B2. `workflows/backup-db.yml` → `supabase/backup-action@v2`
- **Issue:** no public action at this path/tag.
- **Current state:** step unresolved.
- **Update risk:** HIGH / BREAKING.
- **LATER GOAL:** switch to `supabase/setup-cli` + `supabase db dump` (the CLI action IS
  resolvable and already pinned elsewhere in this repo).

### B3. `workflows/compliance.yml` → `my-org/.github-shared/.github/workflows/repo-audit.yml@v1`
- **Issue:** calls a **reusable workflow** in a placeholder org (`my-org`) that does not exist.
- **Current state:** workflow will not start.
- **Update risk:** HIGH / BREAKING (reusable-workflow calls cannot be safely rewritten blind).
- **LATER GOAL:** point at the real shared-workflow repo, or vendor the audit steps inline.

### B4. `.github/workflows/multi-provider-review.yml` → `keithah/multi-provider-code-review@v1.3.0`
- **Issue:** repository/tag does not resolve (the inline comment suggests it previously
  tracked `@486a7bd`).
- **Current state:** step unresolved.
- **Update risk:** MEDIUM — the workflow is a niche AI code-review integration.
- **LATER GOAL:** confirm the correct action source with the maintainer and pin it.

### B5. `.github/workflows/SBOM.yml` → `advanced-security/spdx-dependency-submission-action@5d6e7f8a…`
- **Issue:** the SHA here is a **fabricated 40-hex string** (`5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e`
  — a sequential pattern, not a real commit) and the repository does not resolve.
- **Current state:** NOT modified. The step cannot run.
- **Update risk:** HIGH — replacing it needs a decision about which SBOM tool is intended.
- **LATER GOAL:** replace with `anchore/sbom-action` or the official
  `advanced-security/sbom-generator-action` in v1.5.x.

---

## Category C — Pre-existing corrupt YAML (🟠 → these workflows never ran)

These 8 files fail `yaml.safe_load` **on `main` before this update** and were left untouched
so the diff stays reviewable. My automation read them, could not parse them, and skipped
rather than risk corrupting an already-broken file. Note the two pairs of near-duplicate
filenames — a rename appears to have gone wrong at some point.

### C1. `.github/workflows/auto-changelog.yml`
- **Issue:** `mapping values are not allowed here` — the file begins with a stray `yaml`
  token before the real content.
- **Current state:** invalid; workflow is silently ignored by GitHub.
- **Update risk:** MEDIUM.
- **LATER GOAL:** repair to valid YAML; it duplicates the working `changelog.yml` — consider
  deleting instead.

### C2. `.github/workflows/check-absolute-paths.yml`
- **Issue:** `while scanning a simple key` — unquoted colon in a value.
- **Current state:** invalid; also duplicates the valid `Check-Absolute-Path.yml`.
- **Update risk:** LOW (duplicate — safe to delete the broken twin).
- **LATER GOAL:** delete this duplicate, keep `Check-Absolute-Path.yml`.

### C3. `.github/workflows/commit-pr-metadata.yml`
- **Issue:** `while scanning a simple key` — same quoting defect.
- **Current state:** invalid.
- **Update risk:** MEDIUM.
- **LATER GOAL:** repair in v1.5.x.

### C4. `.github/workflows/post-or-update-comment.yml`
- **Issue:** `while scanning a simple key`.
- **Current state:** invalid; note there is also a valid
  `.github/workflows/post-merge.yml` doing similar work.
- **Update risk:** MEDIUM.
- **LATER GOAL:** repair or consolidate with `post-merge.yml`.

### C5. `.github/workflows/telegram-alerts.yml`
- **Issue:** `while parsing a block collection` — this file is a fragment with no top-level
  `name:` / `on:` mapping, so it is not a workflow at all.
- **Current state:** invalid; never runs.
- **Update risk:** LOW.
- **LATER GOAL:** convert to a proper workflow or move it under `docs/` as an example.

### C6–C8. `workflows/LineUILog.yml`, `workflows/cleanup.yml`, `workflows/refreshpr.yml`
- **Issue:** all three parse as **bare fragments** (`not a mapping`) — no `name:`/`on:`/`jobs:`.
- **Current state:** invalid; not recognized as workflows.
- **Update risk:** LOW.
- **LATER GOAL:** the entire top-level `workflows/` directory is a **stale duplicate** of
  `.github/workflows/` (36 files, 30 never executed). Recommend deleting the directory in
  v1.5.x rather than repairing file-by-file.

---

## Category D — Duplicate / shadowed workflow trees (🟡)

### D1. `workflows/` (top-level, 36 files) — duplicates `.github/workflows/`
- **Issue:** GitHub only reads workflows from `.github/workflows/`. This entire directory is
  dead weight that also confuses tooling (it caused several of the "unpinned action" hits in
  the audit, and its `CI.yml` shadows the real `ci.yml` in name).
- **Current state:** NOT deleted. Files inside were still hardened (SHA-pinned, permissions
  added) so that nothing in the repo is left in a worse state than before, but they remain
  inactive.
- **Update risk:** HIGH — deleting 36 files is a large, irreversible surface change that
  deserves the owner's explicit yes.
- **LATER GOAL:** delete `workflows/` entirely in v1.5.x after confirming no external tool
  references it.

### D2. `.gitHub/` (capital H) — 1 file: `.gitHub/workflows/AdminPR.yml`
- **Issue:** a second, differently-capitalized GitHub directory. On a case-insensitive
  filesystem this collides with `.github/`; on GitHub it is simply ignored.
- **Current state:** NOT modified beyond SHA-pinning.
- **Update risk:** MEDIUM — renaming it could surprise a contributor on macOS/Windows.
- **LATER GOAL:** merge the one useful workflow into `.github/workflows/` and delete `.gitHub/`.

---

## Category E — Pre-existing build / test failures (🟠)

Neither was introduced or fixed by this update; both were confirmed identical on a clean
`HEAD` checkout (via `git stash`) and are therefore out of scope for a "zero-regression"
change. They are recorded here so they are not mistaken for update fallout.

### E1. Next.js build — `app/page.tsx doesn't have a root layout`
- **Issue:** `app/` contains `page.tsx`, `api/`, `dashboard/`, `studio/`, components — but
  **no `app/layout.tsx`**. Next.js 15 (and 13+) App Router requires a root layout.
- **Current state:** `pnpm build` fails at the `next build` step. `tsup` (the package
  artifact) succeeds regardless.
- **Update risk:** MEDIUM — adding a root layout is additive, but it is a real feature change
  with styling implications, and `app/` mixes Kotlin (`app/core/network/AuthInterceptor.kt`,
  `app/data/**`) with Next.js pages, so the tree needs a decision first.
- **LATER GOAL:** add `app/layout.tsx` (and `app/globals.css`), or split the Kotlin Android
  sources out of `app/` so Next.js gets a clean App Router tree. v1.5.x.

### E2. Vitest suite — 12 files fail, 3 tests fail
- **Issue:** the test files import `jest` globals (`jest.clearAllMocks()`, `jest.fn()`) but
  the project runs **Vitest** with no Jest compatibility shim configured
  (`globals` / `globals: true` + `vi` not set up). `vitest.config.js` does not enable
  `globals`, and the tests never import from `vitest`.
- **Current state:** `pnpm test` fails — pre-existing, identical before and after.
- **Update risk:** LOW-MEDIUM — fixing means either enabling `globals: true` in
  `vitest.config.js` and aliasing `jest` → `vi`, or rewriting the test imports.
- **LATER GOAL:** in v1.5.x add `globals: true` to `vitest.config.js` and a
  `globalThis.jest = vi` shim in a setup file, **or** migrate the 12 files to
  `import { vi, describe, it, expect } from 'vitest'`. This is the single highest-value test
  fix available.

---

## Category F — Out-of-scope major upgrades (🟡)

Held back deliberately: these are **major** version bumps that carry breaking changes and
would violate the "no breaking changes" rule of this task.

### F1. `next` 15.5.25 → 16.3.5
- **Update risk:** HIGH / BREAKING — Next 16 removes/renames APIs, changes defaults, and
  would need a migration pass (async `params`, caching defaults, etc.).
- **LATER GOAL:** dedicated upgrade PR on a branch with the E1 layout fix already in place.

### F2. `react` / `react-dom` 18.3.1 → 19.3.0
- **Update risk:** HIGH / BREAKING — React 19 changes ref handling, removes legacy APIs, and
  requires compatible `@types/react`. Must move **together with** Next 16.
- **LATER GOAL:** same PR as F1.

### F3. `typescript` 5.9.3 → 7.0.2
- **Update risk:** HIGH — a two-major jump with new strictness defaults and a different
  compiler backend; would surface unknown type errors across `src/` and the legacy paths.
- **LATER GOAL:** after F1/F2 are settled, upgrade on its own branch.

### F4. `vitest` 1.6.1 → 5.0.0
- **Update risk:** HIGH / BREAKING — four majors of config and API change.
- **LATER GOAL:** fold into the E2 test repair so the suite is green before the bump.

### F5. `@supabase/ssr` 0.5.2 → 0.12.7
- **Update risk:** MEDIUM-HIGH — pre-1.0 package, so a 0.5 → 0.12 move is effectively major
  (cookie-helper API changed).
- **LATER GOAL:** v1.6.x, with the auth middleware re-tested.

### F6. `@vercel/analytics` 1.6.1 → 2.0.1 · `@vercel/speed-insights` 1.3.1 → 2.0.0
- **Update risk:** MEDIUM — both are major bumps to client-side injection components.
- **LATER GOAL:** v1.6.x, together.

---

## What the owner should do first

1. **Rotate the credentials in `.env.local` and check `service_account.json`** (A1, A3) —
   everything else can wait; this cannot.
2. **Decide on `workflows/` and `.gitHub/`** (D1, D2) — one word from you and I will delete
   the stale trees in a follow-up PR.
3. **Fix the two build/test failures** (E1, E2) — E2 is a ~15-minute change and unlocks the
   whole test suite.
4. **Then** the major upgrades (F1–F6) as one planned migration.
