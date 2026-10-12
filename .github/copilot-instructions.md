# Copilot Instructions — Zyntro Media AI

> Org-level instructions for all repositories under **Zyntro-Media-AI**.  
> Copilot must follow these conventions unless a repo-level `copilot-instructions.md` overrides them.

---

## 1. Stack & Runtime

- **Frontend**: Next.js 14+ (App Router). Use Server Components by default; add `"use client"` only when necessary (event handlers, hooks, browser APIs).
- **Language**: TypeScript strict mode (`"strict": true`). No `any` unless explicitly commented with a reason.
- **Backend / DB**: Supabase (PostgreSQL). Use the `@supabase/supabase-js` v2 client. Prefer server-side client (`createServerClient`) in Server Components and Route Handlers.
- **AI inference**: Groq SDK (`groq-sdk`) for LLM calls. Do not use OpenAI SDK unless the model is OpenAI-only.
- **Styling**: Tailwind CSS. No inline `style={}` unless dynamic values require it.
- **Package manager**: npm. Do not suggest yarn or pnpm commands.
- **Runtime env**: Node.js 20 LTS. Code must run in Termux (Android) without native binary dependencies where possible.

---

## 2. Project Structure (Next.js repos)

```
app/
  (routes)/          # route groups
  api/               # Route Handlers
components/
  ui/                # shadcn/ui primitives
  [feature]/         # feature-specific components
lib/
  supabase/          # client + server helpers
  groq/              # Groq client + prompt builders
  utils/             # pure helpers
types/               # shared TypeScript types
```

- Keep components under 200 lines. Split into sub-components if larger.
- Co-locate types with their feature; export shared types from `types/`.
- Server actions go in `app/actions/` with `"use server"` directive.

---

## 3. TypeScript Conventions

- Export named types, not default types.
- Prefer `interface` for object shapes, `type` for unions/intersections.
- Use `z.infer<typeof Schema>` (Zod) for API request/response types.
- Always type Supabase query returns explicitly — do not rely on inferred `any` from `.data`.

```ts
// ✅ Good
const { data, error } = await supabase
  .from('videos')
  .select('id, title, status')
  .returns<Video[]>()

// ❌ Bad
const { data } = await supabase.from('videos').select('*')
```

---

## 4. Supabase Patterns

- Use Row Level Security (RLS) on every table. Never bypass with service role key on the client.
- Service role key (`SUPABASE_SERVICE_ROLE_KEY`) is server-only — never import in `"use client"` files.
- Wrap multi-step DB operations in a Postgres function (RPC) rather than multiple round-trips.
- Always handle `error` from Supabase calls before accessing `data`.
- Use `supabase.storage` for file uploads; never store binary in the DB.

---

## 5. AI Pipeline (Groq + FAL + RunwayML + others)

- All AI calls must go through `lib/groq/` or `lib/ai/[provider]/` — no direct SDK calls from components.
- Prompt templates live in `lib/groq/prompts/` as exported `const` strings or builder functions.
- Never hardcode model IDs in components; import from `lib/ai/models.ts`.
- Always set `max_tokens` and `temperature` explicitly — never rely on provider defaults.
- Wrap every external AI call in try/catch and return a typed `Result<T, Error>` pattern.
- Log provider, model, latency, and token usage (no PII) via a centralised `lib/logger.ts`.

```ts
// lib/ai/models.ts
export const MODELS = {
  groq: {
    fast: 'llama-3.1-8b-instant',
    smart: 'llama-3.3-70b-versatile',
  },
  fal: {
    imageGen: 'fal-ai/flux/schnell',
  },
} as const
```

---

## 6. Code Style & Review Rules

- **No commented-out code** in PRs. Delete it or use a `// TODO(name): reason` comment.
- **No `console.log`** in production code. Use `lib/logger.ts` instead.
- Functions must be pure where possible. Side effects belong in hooks or server actions.
- Max function length: 40 lines. Extract helpers if longer.
- Boolean variable names must start with `is`, `has`, `can`, or `should`.
- Async functions must always `await` — no floating promises.
- Error messages must be human-readable strings, not raw error objects.

---

## 7. Environment Variables

- All env vars must be declared in `.env.example` with placeholder values and a comment.
- Client-side vars must be prefixed `NEXT_PUBLIC_`.
- Never access `process.env` directly in components — wrap in `lib/config.ts`.

```ts
// lib/config.ts
export const config = {
  groqApiKey: process.env.GROQ_API_KEY!,
  supabaseUrl: process.env.NEXT_PUBLIC_SUPABASE_URL!,
  // ...
} as const
```

---

## 8. Testing

- Use **Vitest** for unit tests. Jest is not used in this org.
- Test files live next to the source: `lib/utils/format.test.ts`.
- Every exported util function must have at least one test.
- Mock Supabase and Groq clients in tests — never call real APIs in test suite.
- Run tests with `npm test` (mapped to `vitest run`).

---

## 9. CI / GitHub Actions

- Workflow files live in `.github/workflows/`.
- Every PR must pass: `lint` → `type-check` → `test` → `build` in that order.
- Use `actions/cache` for `node_modules` keyed on `package-lock.json` hash.
- Secrets are accessed via `${{ secrets.NAME }}` — never hardcode in YAML.
- Notify on failure via Slack webhook (`SLACK_WEBHOOK_URL` secret).

---

## 10. Security

- Never commit `.env` files. `.env.example` only.
- Sanitise all user inputs before passing to SQL or AI prompts.
- Use Supabase RLS + JWT claims for authorization — never roll custom auth middleware.
- Dependabot alerts must be resolved within 7 days for high/critical severity.
- No `eval()`, `dangerouslySetInnerHTML` without sanitisation, or dynamic `require()`.

---

## 11. Git & PR Conventions

- Branch naming: `feat/`, `fix/`, `chore/`, `docs/` prefixes.
- Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/): `feat(scope): description`.
- PRs must reference an issue: `Closes #123`.
- Keep PRs small — one logical change per PR.
- Semantic Release is used for versioning; do not manually bump `package.json` version.

---

## 12. What Copilot Should NOT Do

- Do not suggest `pages/` directory patterns — this org uses App Router only.
- Do not use `getServerSideProps` or `getStaticProps`.
- Do not suggest `axios` — use native `fetch` or the provider SDK.
- Do not generate migration files manually — use `supabase db diff` instead.
- Do not add `// eslint-disable` without a specific rule name and reason.
- Do not suggest storing secrets in `next.config.js` env section.
### Zyntro Media AI — Copilot Instructions: Debug & Rerun Jobs

เป้าหมายคือเพิ่มมาตรฐาน CI Failure Diagnosis, Safe Job Reruns และ Automated Recovery ให้ทุก repository ภายใต้องค์กร `Zyntro-Media-AI` โดยไม่ลดระดับความปลอดภัยของ CI/CD และไม่เปลี่ยนลำดับการตรวจสอบเดิม

The design adds a consistent recovery workflow to your existing pipeline:

`Lint → Type-check → Test → Build → Diagnose → Rerun → Verify`

หลักการสำคัญคือ Copilot ต้องตรวจสอบสาเหตุของความล้มเหลวก่อน rerun, แยก transient failures ออกจาก code defects และไม่ rerun deployment หรือขั้นตอนที่มี side effects โดยอัตโนมัติอย่างไม่มีเงื่อนไข

### 1\. Add this section to organization-level Copilot instructions

ไฟล์แนะนำ: `COPILOT_INSTRUCTIONS.md` ในเอกสารมาตรฐานขององค์กร หรือเพิ่มหัวข้อนี้ในไฟล์ organization-level instructions ที่คุณใช้อยู่จริง โดยเก็บไฟล์ `.github/copilot-instructions.md` ของแต่ละ repository สำหรับกฎเฉพาะโครงการ

## 13. CI Debugging, Failed Job Reruns & Recovery

### 13.1 Debugging Requirements
- When a GitHub Actions job fails, inspect the workflow run, failed job, failed step, annotations, and relevant logs before recommending a fix.
- Identify the exact failure category: lint, type-check, test, build, dependency installation, cache, network, permissions, secrets, runner, timeout, or deployment.
- Distinguish transient infrastructure failures from deterministic code or configuration defects.
- State the root cause, supporting log evidence, affected files, proposed fix, and verification steps.
- Never claim a root cause is confirmed without supporting evidence. Label uncertain diagnoses as hypotheses.
- Never expose secret values, access tokens, credentials, environment dumps, or sensitive log contents in comments or summaries.

### 13.2 Safe Rerun Policy
- Prefer rerunning only failed jobs when successful jobs do not need to be repeated.
- Use a full workflow rerun only when upstream state, artifacts, dependencies, or job relationships require it.
- Rerun a failed job only after reviewing its failure reason and checking whether its operations are safe to repeat.
- Automatically retry only explicitly classified transient, idempotent operations with bounded attempts and backoff.
- Use a maximum of two automatic retries after the initial attempt unless a repository-specific policy explicitly permits more.
- Do not automatically rerun deterministic failures such as lint errors, TypeScript errors, failing tests, invalid YAML, missing configuration, or reproducible build errors.
- Never automatically rerun production deployment, database migrations, destructive operations, or other non-idempotent actions without an explicit safety mechanism and authorization.
- Do not change permissions, disable required checks, weaken branch protection, or skip security gates to make a rerun pass.
- Record the original run ID, attempt number, failed job, failure category, reason for rerun, and final result.

### 13.3 Rerun Decision Matrix
- Transient network or service failure: inspect logs; retry only if the operation is safe.
- Runner interruption or infrastructure failure: rerun the affected job after confirming that the environment is safe.
- Dependency installation failure: inspect package-lock.json, registry access, and cache state before retrying.
- Lint or type-check failure: fix the source or configuration; rerun the required checks.
- Unit or integration test failure: reproduce and diagnose the failing test before rerunning.
- Build failure: inspect compiler output, dependency versions, environment configuration, and build artifacts.
- Permission or secret failure: correct authorization or configuration through the approved settings process.
- Production deployment failure: stop, inspect deployment state, verify idempotency, and require appropriate authorization before retrying.

### 13.4 GitHub Actions Rerun Operations
- Use the GitHub Actions UI or the official REST API to rerun failed jobs.
- Use the failed-jobs endpoint when successful jobs should remain untouched.
- Use the individual-job rerun endpoint when only one failed or cancelled job needs to be retried.
- Verify that the selected run belongs to the intended repository, workflow, branch, and commit.
- Require Actions write permission for API-based reruns and use the least-privilege credential available.
- Never store a GitHub token in source code, workflow YAML, logs, or artifacts.
- Treat rerun requests as operational actions, not as permission to modify application code automatically.

### 13.5 CI Observability
- Publish a concise GitHub Actions job summary containing the failure category, failed step, sanitized evidence, remediation, and rerun outcome.
- Upload diagnostic artifacts only when useful and ensure they exclude credentials and sensitive data.
- Use GitHub annotations to identify actionable failures without duplicating sensitive logs.
- Preserve test reports, coverage reports, and build diagnostics when safe.
- Avoid duplicate notifications. Notify Slack only when SLACK_WEBHOOK_URL is configured, and never print the webhook URL.
- Do not swallow exceptions or convert failed jobs into successful results without explicit, justified policy.

### 13.6 Verification After Recovery
- Confirm the rerun completed and inspect the resulting job conclusions.
- Re-run the complete required validation sequence: lint → type-check → test → build.
- Confirm that the successful run corresponds to the intended commit SHA.
- Treat a successful rerun as evidence of recovery, not proof that an intermittent defect is permanently resolved.
- Document recurring failures and create an issue when a durable fix is required.

### 13.7 Copilot Reporting Format
For each CI failure, report:
1. Workflow name and run ID.
2. Failed job and step.
3. Failure category and evidence.
4. Confirmed root cause or clearly labeled hypothesis.
5. Recommended code or configuration change.
6. Rerun scope: single job, failed jobs, or full workflow.
7. Safety checks and required permissions.
8. Verification result and remaining risks.

### 13.8 Safety Boundaries
- Diagnose first, repair second, rerun third, verify last.
- Never fabricate a rerun result or claim that a job was rerun without an actual API or UI confirmation.
- Never push fixes, approve pull requests, deploy production, or change repository security settings without the appropriate authorization.
- If automated recovery is unavailable, provide the exact UI steps or API request needed for an authorized maintainer.

### 2\. Add a manual failed-job rerun workflow

ไฟล์ `.github/workflows/rerun-failed-jobs.yml` นี้ช่วยให้ maintainer สั่ง rerun เฉพาะ failed jobs ผ่าน `workflow_dispatch` ได้ โดยไม่ต้อง rerun งานที่สำเร็จทั้งหมด

This is an optional operational workflow. It does not automatically rerun every failure, and it does not repair source code.

```yaml

name: Rerun Failed Jobs

on:
  workflow_dispatch:
    inputs:
      run_id:
        description: "Completed GitHub Actions run ID"
        required: true
        type: string
      confirm_rerun:
        description: "Confirm that the failed jobs are safe to rerun"
        required: true
        type: boolean
        default: false

permissions:
  actions: write
  contents: read

concurrency:
  group: rerun-failed-jobs-${{ inputs.run_id }}
  cancel-in-progress: false

jobs:
  rerun:
    name: Validate and Rerun Failed Jobs
    runs-on: ubuntu-latest
    timeout-minutes: 5

    steps:
      - name: Validate request
        env:
          RUN_ID: ${{ inputs.run_id }}
          CONFIRM_RERUN: ${{ inputs.confirm_rerun }}
        shell: bash
        run: |
          set -euo pipefail

          if [[ ! "$RUN_ID" =~ ^[0-9]+$ ]]; then
            echo "::error::run_id must contain only digits."
            exit 1
          fi

          if [[ "$CONFIRM_RERUN" != "true" ]]; then
            echo "::error::Explicit rerun confirmation is required."
            exit 1
          fi

      - name: Inspect target run
        env:
          GH_TOKEN: ${{ github.token }}
          RUN_ID: ${{ inputs.run_id }}
        shell: bash
        run: |
          set -euo pipefail

          gh api \
            "repos/${GITHUB_REPOSITORY}/actions/runs/${RUN_ID}" \
            --jq '{
              id: .id,
              repository: .repository.full_name,
              workflow: .name,
              branch: .head_branch,
              commit: .head_sha,
              status: .status,
              conclusion: .conclusion
            }' > "$RUNNER_TEMP/run-summary.json"

          cat "$RUNNER_TEMP/run-summary.json"

          node -e '
            const fs = require("node:fs");
            const run = JSON.parse(
              fs.readFileSync(process.argv[1], "utf8")
            );

            if (run.repository !== process.env.GITHUB_REPOSITORY) {
              throw new Error("Repository mismatch.");
            }

            if (run.status !== "completed") {
              throw new Error("Target run is not completed.");
            }

            if (run.conclusion === "success") {
              throw new Error("Target run has no failed jobs to recover.");
            }
          ' "$RUNNER_TEMP/run-summary.json"

      - name: Rerun failed jobs
        env:
          GH_TOKEN: ${{ github.token }}
          RUN_ID: ${{ inputs.run_id }}
        shell: bash
        run: |
          set -euo pipefail

          gh api \
            --method POST \
            "repos/${GITHUB_REPOSITORY}/actions/runs/${RUN_ID}/rerun-failed-jobs"

          echo "Rerun request accepted by GitHub."
```

### Operational safeguards

* Use this workflow only for failures that are safe to repeat.

* Run it from a trusted branch and restrict who can initiate it through repository permissions and organization policy.

* The workflow validates the target run and requires explicit confirmation, but confirmation does not prove that a deployment or migration is idempotent.

* The API response confirms that GitHub accepted the rerun request; it does not confirm that the rerun succeeded.

* This workflow does not poll for completion. Verify the target run separately in Actions.

* A GitHub Actions rerun may reuse the original workflow context and commit. It does not automatically apply fixes committed after the original run.

Official reference: [GitHub REST API — Rerun failed jobs](https://docs.github.com/en/rest/actions/workflow-runs#re-run-failed-jobs-from-a-workflow-run).

### 3\. Recommended debugging architecture

GitHub Actions Failure

Run ID · Job ID · Failed step · Logs

Failure Classifier

Transient / Code defect / Permission / Infrastructure

Safe transient

Bounded retry

Code defect

Fix and validate

Permission issue

Authorized correction

Production failure

Stop and review

Rerun → Verify → Audit

Record outcome and preserve required CI gates

### 4\. Implementation order

* Update the organization-level Copilot instructions.

* Add the manual rerun workflow to a test repository first.

* Test invalid run IDs, successful runs, permission failures, and transient failures.

* Confirm that only the intended failed jobs are rerun.

* Add sanitized diagnostic summaries and Slack notifications.

* Roll out to other repositories after maintainer review.

ข้อควรระวัง: GitHub organization-level Copilot instructions and GitHub Actions permissions are separate controls. Instructions guide generated code and recommendations; they do not enforce authorization by themselves.

Next recommended improvement: Add a `debug-failure.yml` workflow that gathers job and step metadata, classifies failures, and publishes a sanitized diagnostic report before a maintainer decides whether to rerun. This separates diagnosis from execution and makes recovery auditable across the organization.
