Canonical workflows (consolidate duplicates into these):
- ci.yml → CrystalCastleCopilot.yml (validate → ai-tests → build → security → deploy)
- docker-publish.yml → build & push GHCR (SHA tag)
- sandbox-preview.yml → PR preview deploy + cleanup (MISSING — should be added)
- ai-auto-repair.yml → failure → LLM patch → PR → rerun (MISSING — should be added)
- trivy-image-scan.yml, lighthouse-audit.yml, release-drafter.yml (recommended additions)

DUPLICATES to merge: changelog×3, absolute-path×2, log-summary×2, ai-pipeline×3.
Rules: SHA-pin all actions, permissions: least-privilege, concurrency group per ref.
