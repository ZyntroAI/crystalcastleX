
---

### 📄 environment-vars.md
```markdown
# Netlify Environment Variables

## Overview
Store configuration, secrets, and API keys without committing them to Git.

## How to Set Variables

### UI Method
1. Go to **Site settings → Environment variables**
2. Click **Add environment variable**
3. Enter key and value
4. Select deploy context:
   - ✅ All scopes
   - Production only
   - Deploy previews only
   - Branch deploys only

### netlify.toml Method
```toml
[build.environment]
NODE_VERSION = "20"
PNPM_VERSION = "9"
