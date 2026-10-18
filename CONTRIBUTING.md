# Contributing to CrystalCastle X

## 🛡️ Security Practices Before Committing

### Before You Push Code:
- ✅ **Never commit secrets** — API keys, passwords, tokens, `.env` files
- ✅ **Check before committing** — Run `gitleaks detect` locally or use pre-commit hooks
- ✅ **Use environment variables** — Keep secrets in `.env` (already in `.gitignore`), use `.env.example` as template only
- ✅ **Review your code** — Check for commented-out credentials, debug endpoints, or personal data

### What Gets Caught Automatically:
- Gitleaks scans **every push** for API keys, tokens, passwords
- `npm audit` runs on all PRs targeting `main`
- CodeQL analyzes JavaScript/TypeScript and Python for security issues
- Dependency Review blocks PRs with known vulnerabilities

### If You Accidentally Commit a Secret:
1. **Revoke the credential immediately** — Rotate API keys/passwords
2. **Do NOT force-push** — Contact repository maintainers
3. Report via **GitHub Security Advisory** — Go to: Security → advisories → New draft

### Workflow Requirements:
- All checks must pass before merging
- Code review required for all changes
- Security team review for: `SECURITY.md`, CI workflows, dependency version bumps
