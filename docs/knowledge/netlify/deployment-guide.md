# Netlify Deployment Guide

## Overview
Step-by-step instructions for deploying sites and apps to Netlify.

## Prerequisites
- A Netlify account
- Your project in a Git repository (GitHub, GitLab, Bitbucket)
- Netlify CLI installed: `npm install -g netlify-cli`

## Deployment Methods

### 1. Git-Based Deployment (Recommended)
1. Log in to Netlify
2. Click **Add new site → Import an existing project**
3. Connect your Git provider
4. Select your repository
5. Configure:
   - **Base directory**: Leave blank unless in a subfolder
   - **Build command**: `npm run build` / `pnpm build` / `yarn build`
   - **Publish directory**: `dist`, `build`, or `.output`
6. Click **Deploy site**

### 2. Manual Upload
- Drag & drop your publish folder at **app.netlify.com/drop**
- Or use CLI: `netlify deploy --prod`

### 3. CLI Deployment
```bash
# Login
netlify login

# Initialize
netlify init

# Deploy to production
netlify deploy --prod

# Deploy preview
netlify deploy
