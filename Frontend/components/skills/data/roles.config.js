// ==========================================
// 🧹 CHORES & MAINTENANCE DATA
// ==========================================
export const CHORES = {
  daily: [
    { id: 'c-d-1', text: 'Pull latest changes from main before starting work' },
    { id: 'c-d-2', text: 'Close unused tabs/branches; delete temp files' },
    { id: 'c-d-3', text: 'Commit work with clear message at end of day' },
    { id: 'c-d-4', text: 'Update task status: To Do → In Progress → Done' },
    { id: 'c-d-5', text: 'Check for PR reviews or pending messages' },
    { id: 'c-d-6', text: 'Log any blockers or issues immediately' },
  ],
  weekly: [
    { id: 'c-w-1', text: 'Docs: Fix typos; update README; archive old drafts' },
    { id: 'c-w-2', text: 'Code: Remove debug code; organize messy files' },
    { id: 'c-w-3', text: 'Security: Run secret scan; check for exposed credentials' },
    { id: 'c-w-4', text: 'Dependencies: Review minor updates; patch safely' },
    { id: 'c-w-5', text: 'Files: Clear downloads; move stray files to correct folders' },
    { id: 'c-w-6', text: 'Progress: Update your skill card checkmarks' },
  ],
  monthly: [
    { id: 'c-m-1', text: 'Update major dependencies; run full test suite' },
    { id: 'c-m-2', text: 'CI/CD: Review logs; fix flaky jobs; remove unused workflows' },
    { id: 'c-m-3', text: 'Docs: Add missing info; update outdated guides' },
    { id: 'c-m-4', text: 'Git: Clean up stale branches; prune merged PRs' },
    { id: 'c-m-5', text: 'Backups: Verify exports; confirm scheduled tasks run' },
    { id: 'c-m-6', text: 'Self-assessment: Review your level; set next goals' },
  ],
  project: [
    { id: 'c-p-1', text: 'Docs: Fix broken links & update Table of Contents' },
    { id: 'c-p-2', text: 'Docs: Archive outdated pages to /archive/' },
    { id: 'c-p-3', text: 'Code: Lint & format; fix warnings before release' },
    { id: 'c-p-4', text: 'Code: Update CHANGELOG.md with notable changes' },
    { id: 'c-p-5', text: 'Security: Audit dependencies for vulnerabilities' },
    { id: 'c-p-6', text: 'Tests: Run full suite; confirm release readiness' },
  ]
};
