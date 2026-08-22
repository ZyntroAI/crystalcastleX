Contributing to install-crystal

Thank you for your interest in contributing to "install-crystal".

"install-crystal" is a GitHub Action for installing the Crystal programming language. Contributions should preserve the Action's reliability, security, portability, and compatibility across supported GitHub Actions environments.

This guide explains how to propose changes, set up a development environment, run checks, write tests, prepare pull requests, and contribute documentation.

Before you begin

Review the project

Before making changes, review:

- "README.md"
- "action.yml"
- "package.json"
- "index.js"
- Existing tests
- Existing GitHub Actions workflows
- Open and closed issues
- Recent pull requests

Understand how the Action currently downloads, caches, selects, and installs Crystal before changing related code.

Check existing issues

Start with an existing issue whenever possible.

For bug fixes:

1. Find the relevant bug report.
2. Confirm that the issue is still reproducible.
3. Comment on the issue if clarification is required.
4. Keep the implementation focused on the reported problem.

For new features:

1. Open or locate a feature request.
2. Explain the use case.
3. Discuss compatibility and security implications.
4. Wait for maintainer feedback before implementing large changes.

Small documentation, test, or maintenance changes may not require a separate issue when project maintainers consider them straightforward.

Fork and create a branch

Fork the repository and clone your fork:

git clone https://github.com/YOUR_USERNAME/install-crystal.git
cd install-crystal

Add the upstream repository:

git remote add upstream https://github.com/crystal-lang/install-crystal.git

Create a feature branch:

git fetch upstream
git checkout -b fix/your-change upstream/main

Use a descriptive branch name.

Examples:

fix/windows-install
fix/cache-key
fix/version-resolution
feat/crystal-version-input
docs/contributing
test/platform-detection

Avoid using "main" for development work.

Development environment

Prerequisites

You need:

- Git
- Node.js 20 or newer
- npm
- A supported operating system for the functionality being changed
- Docker or another isolated environment when required for integration testing

Check your versions:

node --version
npm --version
git --version

The repository's "package.json" is the source of truth for supported Node.js versions.

Install dependencies

Use the committed lockfile:

npm ci

Do not replace "npm ci" with "npm install" when reproducing CI failures.

If dependencies need to be changed, update both:

package.json
package-lock.json

Then verify the installation:

npm ci

Project structure

The repository is a GitHub Action rather than a large application or monorepo.

A typical structure is:

install-crystal/
├── action.yml
├── index.js
├── package.json
├── package-lock.json
├── eslint.config.js
├── test/
│   ├── *.test.js
│   └── ...
├── README.md
├── CONTRIBUTING.md
├── LICENSE
└── .github/
    └── workflows/
        ├── ci.yml
        └── ...

Keep implementation changes focused and avoid introducing additional layers unless they provide a clear maintenance or testing benefit.

Understanding the Action

The primary public interface is defined by "action.yml".

Before changing implementation code, check:

- Action inputs
- Default values
- Outputs
- Runtime
- Entrypoint
- Supported platforms
- Required permissions
- Documentation examples

Changes to "action.yml" can be breaking changes even when the JavaScript implementation appears small.

When changing an input or output, update the relevant documentation and tests.

Development workflow

The normal workflow is:

Issue
  ↓
Fork
  ↓
Feature branch
  ↓
Implement
  ↓
Add/update tests
  ↓
Update documentation
  ↓
Run preflight
  ↓
Commit
  ↓
Pull request
  ↓
CI and review
  ↓
Maintainer approval
  ↓
Merge

Keep changes small and independently reviewable.

Code quality

The project uses ESLint for static analysis.

Run linting with:

npm run lint

Fix automatically supported issues with:

npm run lint -- --fix

Do not disable an ESLint rule simply to make CI pass.

If a rule needs to be changed, explain why the existing rule is unsuitable and keep the exception as narrow as possible.

Syntax checking

The project runs JavaScript as an ES module.

Check the main entrypoint with:

npm run check

The equivalent direct command is:

node --check index.js

Syntax checking should be performed before submitting a pull request.

Testing

Tests should verify behavior rather than implementation details.

Run the test suite with:

npm test

The project uses Node.js's built-in test runner where practical.

A typical test can use:

import test from 'node:test';
import assert from 'node:assert/strict';

test('example behavior', () => {
  assert.equal(1 + 1, 2);
});

Tests should cover important behavior such as:

- Version parsing
- Version comparison
- Platform detection
- Architecture detection
- Download URL generation
- Cache behavior
- Input handling
- Error handling
- Invalid versions
- Unsupported platforms
- Network failures
- File-system failures

Tests must not require real production credentials.

Avoid tests that download large external artifacts unless they are explicitly classified as integration tests.

Integration testing

Changes that affect actual installation behavior should be tested in an environment that represents the target platform.

Integration tests may validate:

GitHub Action
    ↓
Input resolution
    ↓
Platform detection
    ↓
Crystal artifact resolution
    ↓
Download
    ↓
Cache
    ↓
Installation
    ↓
Crystal executable

Integration tests should be isolated from unit tests where possible.

Tests that depend on external services should:

- Fail with useful diagnostics.
- Avoid exposing credentials.
- Avoid modifying unrelated files.
- Avoid depending on a developer's local environment.
- Clean up temporary files.
- Avoid destructive operations.

Preflight

Before opening a pull request, run:

npm run preflight

The preflight command should be treated as the project's local quality gate.

It should include, as applicable:

ESLint
JavaScript syntax validation
Unit tests
Other repository validation

A contributor should not open a ready-for-review PR while preflight is failing.

The local command and CI command should remain aligned so that:

npm run preflight

provides a reliable indication of whether the PR is ready.

Security

GitHub Actions execute code in CI environments that may have access to repository contents, tokens, artifacts, and environment variables.

Treat pull requests as potentially untrusted code.

Do not execute untrusted pull request code locally while sensitive credentials are available.

Security-sensitive areas

Pay particular attention to changes involving:

- "child_process"
- Shell commands
- "exec"
- "spawn"
- Downloaded files
- Archive extraction
- Redirects
- URLs
- HTTP responses
- GitHub tokens
- Environment variables
- File-system writes
- Temporary directories
- Cache paths
- "action.yml"
- Workflow permissions

Command execution

Avoid constructing shell commands from untrusted input.

Prefer APIs that accept argument arrays rather than shell strings.

Validate inputs before passing them to operating-system commands.

Downloads

When downloading Crystal releases:

- Validate URLs.
- Prefer trusted release sources.
- Use HTTPS.
- Validate downloaded content where practical.
- Avoid silently following unexpected redirects.
- Do not execute downloaded content before validation.
- Keep temporary files isolated.

Secrets

Never commit:

API keys
Access tokens
Private keys
Passwords
Credentials
Personal access tokens
GitHub secrets

Use environment variables or GitHub Actions secrets when credentials are genuinely required.

Never print secrets in logs.

GitHub Actions security

Changes to workflow files require additional review.

Keep workflow permissions minimal.

Prefer:

permissions:
  contents: read

when the workflow does not require additional permissions.

Avoid granting write permissions globally when a single job or step can use a narrower permission.

Do not use untrusted pull request data directly inside shell commands.

Caching

Changes involving "@actions/cache" or installation caching should be tested carefully.

A cache key should distinguish relevant dimensions such as:

Crystal version
Operating system
Architecture
Relevant installation configuration

Do not allow one platform or architecture to consume an incompatible cached artifact.

Cache misses should continue to work correctly.

The Action must remain functional when no cache is available.

Cross-platform compatibility

Crystal installation behavior may differ across:

- Linux
- macOS
- Windows
- CPU architectures
- GitHub-hosted runners
- Self-hosted runners

When changing platform-specific behavior:

1. Identify all affected platforms.
2. Add or update platform-specific tests.
3. Avoid assuming Unix shell behavior.
4. Avoid hard-coded path separators.
5. Use Node.js path APIs.
6. Validate architecture handling.
7. Document unsupported combinations.

Prefer portable Node.js APIs over shell-specific commands.

Documentation

Update documentation whenever behavior changes.

User-facing changes should normally update:

- "README.md"
- "action.yml" descriptions
- Examples
- Input/output documentation
- Compatibility information
- Migration notes when necessary

Documentation should explain:

- What changed.
- Why it changed.
- How users should use it.
- Any compatibility limitations.
- Any required configuration.

Keep examples executable and consistent with the current Action interface.

Pull requests

Before opening a PR

Run:

npm ci
npm run lint
npm run check
npm test
npm run preflight

Review the final diff:

git diff

Check the status:

git status

Confirm that no generated files, credentials, local configuration, or unrelated changes are included.

Pull request scope

Keep pull requests:

- Small
- Focused
- Testable
- Independently reviewable

Good:

fix(cache): prevent cross-platform cache collisions

Less useful:

fix installer, update dependencies, refactor tests, rewrite docs, and change CI

Large changes should be split into logical pull requests when practical.

Draft pull requests

Use a Draft Pull Request when:

- The implementation is incomplete.
- You want early architectural feedback.
- Tests are still being developed.
- The API is still being discussed.

Convert the PR to ready for review when the implementation and checks are complete.

Pull request description

A good PR description should explain:

What changed?
Why was it necessary?
How was it tested?
Are there compatibility implications?
Are documentation changes required?

For example:

## Summary

Fix Crystal cache keys so installations on different architectures do not
share incompatible cached artifacts.

## Why

The previous cache key did not include the runner architecture.

## Testing

- npm run lint
- npm run check
- npm test
- Integration test on Linux x64

## Documentation

No user-facing API changes.

Link the relevant issue.

Commit messages

Use Conventional Commits where practical.

Examples:

feat(action): add Crystal version input
fix(cache): include architecture in cache key
fix(download): validate release URL
test(version): cover invalid version input
docs(readme): clarify supported platforms
ci(actions): update Node.js runtime
chore(deps): update action dependencies

Keep commits focused.

Avoid messages such as:

changes
fix
update stuff
work
misc

The future maintainer who has to understand the Git history will thank you, despite being unable to send you coffee.

Reviewing pull requests

Reviewers should consider:

Correctness

- Does the change solve the reported problem?
- Does it preserve existing behavior?
- Are edge cases covered?

Tests

- Are tests included?
- Do tests cover failure cases?
- Are tests deterministic?
- Do integration tests avoid unnecessary external dependencies?

Security

- Is user input validated?
- Are shell commands safe?
- Are downloads trusted?
- Are redirects handled safely?
- Could secrets leak into logs?
- Are workflow permissions minimal?

Compatibility

- Does the change work across supported platforms?
- Does it preserve existing Action inputs and outputs?
- Could the change break existing workflows?

Maintainability

- Is the implementation understandable?
- Does it follow existing project patterns?
- Does it avoid unnecessary dependencies?
- Does it keep the public API stable?

Automated review

Automated tools may be used to identify:

- Common bugs
- Security problems
- Missing tests
- Dependency problems
- Style issues
- Workflow configuration problems

Automated review is supplemental.

It does not replace human review.

Reviewers remain responsible for understanding the behavior and security implications of a change.

Never execute an automated review tool against untrusted code without first considering whether the tool will build or execute that code.

Dependencies

Keep dependencies minimal.

When adding a dependency:

1. Explain why it is necessary.
2. Check whether Node.js provides an equivalent API.
3. Check licensing.
4. Check maintenance status.
5. Check known security issues.
6. Consider bundle/runtime impact.
7. Update "package.json".
8. Update "package-lock.json".
9. Run the complete test suite.

Use:

npm install <package>

when intentionally adding or updating a dependency.

For reproducible CI installs, use:

npm ci

Do not manually edit dependency integrity hashes in "package-lock.json".

Updating dependencies

Before submitting dependency updates:

npm install
npm run preflight

Review:

git diff -- package.json package-lock.json

Avoid unrelated dependency upgrades in feature or bug-fix PRs.

Dependency updates should be isolated when practical.

Releases

Release procedures should be performed by project maintainers unless a maintainer explicitly requests otherwise.

Contributors should not publish packages, tags, or releases using project credentials.

Local release experimentation must use appropriate test credentials and isolated environments.

Reporting security issues

Do not disclose sensitive security vulnerabilities in a public issue before the maintainers have had an opportunity to assess them.

Use the repository's documented private security reporting mechanism when one is available.

Security reports should include:

- A concise description.
- Affected versions.
- Reproduction steps.
- Expected behavior.
- Actual behavior.
- Security impact.
- Relevant logs or proof of concept.
- Suggested mitigation when available.

Do not include secrets or private user information in the report.

Documentation contributions

Documentation changes should:

1. Use clear language.
2. Explain the user's goal.
3. Provide practical examples.
4. Keep commands current.
5. Use correct Markdown syntax.
6. Keep links valid.
7. Match the current "action.yml" interface.

When changing an Action input, update all relevant examples.

Local Git hooks

Contributors may use a local pre-commit hook to prevent accidental commits with failing checks.

For example:

cat > .git/hooks/pre-commit <<'EOF'
#!/bin/sh

if ! npm run preflight; then
  echo "Preflight checks failed. Commit aborted."
  exit 1
fi
EOF

chmod +x .git/hooks/pre-commit

This hook is optional.

Git hooks are local and are not automatically distributed through the repository.

Troubleshooting

"npm ci" fails

Check:

node --version
npm --version

Make sure "package.json" and "package-lock.json" are synchronized.

Try a clean installation:

rm -rf node_modules
npm ci

Do not delete or regenerate the lockfile merely to hide a dependency problem.

ESLint fails

Run:

npm run lint

Read the first reported error and fix the underlying issue.

If the problem is caused by an intentional project-level pattern, discuss the appropriate ESLint configuration change rather than adding an unnecessary inline disable.

Tests fail locally but CI passes

Check:

- Node.js version
- Operating system
- Environment variables
- Working directory
- File permissions
- Network access
- Cached dependencies

Avoid making tests depend on machine-specific behavior.

Action works locally but fails on GitHub Actions

Compare:

- Runner OS
- Architecture
- Node.js version
- Environment variables
- File-system paths
- Permissions
- Network behavior
- Cache state

GitHub-hosted runners should be treated as clean environments.

Contributor checklist

Before opening a ready-for-review pull request:

- [ ] I reviewed related issues and pull requests.
- [ ] My change has a focused scope.
- [ ] I created a dedicated branch.
- [ ] I did not commit secrets or credentials.
- [ ] I updated tests where behavior changed.
- [ ] I updated documentation where necessary.
- [ ] "npm ci" succeeds.
- [ ] "npm run lint" succeeds.
- [ ] "npm run check" succeeds.
- [ ] "npm test" succeeds.
- [ ] "npm run preflight" succeeds.
- [ ] I reviewed the final Git diff.
- [ ] The pull request description explains the reason for the change.
- [ ] The pull request links to the relevant issue when applicable.
- [ ] The PR title follows the project's commit/PR naming conventions.
- [ ] I considered cross-platform compatibility.
- [ ] I considered security implications.
- [ ] I verified that changes to "action.yml" are documented.

Maintainer checklist

Before merging:

- [ ] CI passes.
- [ ] Tests cover the changed behavior.
- [ ] Documentation is up to date.
- [ ] Security implications have been reviewed.
- [ ] Action inputs and outputs remain compatible or the change is explicitly documented.
- [ ] Dependency changes are justified.
- [ ] The PR has an appropriate scope.
- [ ] The change is suitable for the supported platforms.
- [ ] No secrets or sensitive data are present.
- [ ] The final diff contains no unrelated changes.

License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project, subject to the repository's applicable contribution and licensing policies.

See "LICENSE" for the complete license text.

Thank you

Every contribution helps improve the reliability and usability of "install-crystal".

Whether you are fixing a bug, improving platform compatibility, adding tests, updating documentation, or improving CI, focused and well-tested contributions are appreciated.
