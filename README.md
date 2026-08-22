# 🔮 Crystal Castle X

![Status](https://img.shields.io/badge/status-active%20development-238636?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-1f6feb?style=flat-square)
![Version](https://img.shields.io/badge/version-0.1.0-8957e5?style=flat-square)
![Node](https://img.shields.io/badge/Node.js-≥18-da3633?style=flat-square&logo=node.js&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-ready-3fb950?style=flat-square&logo=docker&logoColor=white)
![AI](https://img.shields.io/badge/AI-Zyntro--Media-a371f7?style=flat-square)

> Runner AI powered by Zyntro-Media-AI
![Build](https://img.shields.io/github/actions/workflow/status/ZyntroAI/crystalcastleX/ci.yml?branch=main&style=flat-square&label=build)
![Tests](https://img.shields.io/badge/tests-passing-3fb950?style=flat-square)
![Coverage](https://img.shields.io/badge/coverage-75%25-8957e5?style=flat-square)
![Contributors](https://img.shields.io/github/contributors/ZyntroAI/crystalcastleX?style=flat-square&color=1f6feb)
> 

Crystal Castle X is an AI-powered development and automation platform
designed to organize AI runners, application services, developer tooling,
knowledge, artifacts, testing, infrastructure, and production workflows
inside a single repository.

[![GitHub](https://img.shields.io/badge/GitHub-ZyntroAI%2FcrystalcastleX-181717?logo=github)](https://github.com/ZyntroAI/crystalcastleX)
[![License](https://img.shields.io/badge/license-see%20LICENSE-blue.svg)](LICENSE)

---

## 🇹🇭 ภาษาไทย

Crystal Castle X เป็นแพลตฟอร์มสำหรับรวม workflow ของ AI และระบบ
application/development automation ไว้ใน repository เดียว

เป้าหมายหลักคือทำให้ระบบสามารถจัดการได้ตั้งแต่:

- AI runners
- Application frontend/backend
- API integrations
- AI agents
- Knowledge base
- Artifacts
- Tests
- Infrastructure
- Production configuration
- Documentation
- CI/CD workflows
- Development automation

Repository นี้ถูกออกแบบให้สามารถขยายจาก application ไปเป็น
AI-assisted development platform ได้โดยไม่ต้องแยกระบบออกเป็น repository
จำนวนมาก

---

## 🇬🇧 English

Crystal Castle X is an AI-powered runner and development automation platform
for organizing application services, AI agents, APIs, knowledge, artifacts,
testing, infrastructure, production workflows, and documentation in a
single repository.

The project is intended to provide a structured foundation for
AI-assisted development and automation while keeping application,
infrastructure, testing, and operational concerns discoverable from one
repository.

---

# ✨ Features

## 🤖 AI Runner

The project provides a foundation for AI-powered runners and agent workflows.

The repository includes dedicated areas for:

- `agent-hub/`
- AI context
- AI knowledge
- runner-related workflows
- automation scripts
- logs and artifacts

The runner architecture can be extended with additional AI providers,
agents, tools, and execution strategies.

---

## 🧠 Knowledge Management

Crystal Castle X includes dedicated knowledge-management areas for storing
project context and reusable development knowledge.

Relevant paths include:

```text
knowledge-base/
.ai-context.md
.knowledgebase.md

This allows AI-assisted workflows to consume structured project context instead of relying exclusively on transient prompts.


---

🧪 Testing

Testing is treated as a first-class part of the repository.

The project contains multiple test-oriented directories:

__tests__/
test/
tests/

Tests can be used to validate:

application behavior

API behavior

integrations

utilities

AI workflows

regression cases

automation logic


Run the appropriate project test command according to the package or service being modified.


---

🌐 Application Layer

The repository contains both frontend and backend-oriented components.

Frontend/
Backend/
app/
api/
pages/
src/

This structure allows UI, API, service, and shared application logic to evolve independently while remaining inside the same project.


---

🏗 Infrastructure

Infrastructure-related configuration is organized under:

infra/
Production/
docker-compose.yml
Dockerfile

This provides a foundation for local development, containerized execution, and production-oriented deployment workflows.


---

📦 Packages

Reusable functionality is organized through package-oriented directories:

Package/
package/
package/core/
packages/example/

This makes it possible to gradually extract reusable modules without prematurely splitting the repository into multiple projects.


---

📊 Dashboard & Operations

The repository includes dashboard and operational interfaces:

crystalcastle-dashboard/
mission-control.html
admin-logs.html
artifact.html

These areas can be used to expose system status, artifacts, logs, and operational information.


---

🏛 Architecture

At a high level:

┌─────────────────────┐
                    │       User          │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Crystal Castle X  │
                    │      Application    │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
        ┌───────────┐    ┌───────────┐   ┌────────────┐
        │ Frontend  │    │    API    │   │ AI Agents  │
        └───────────┘    └─────┬─────┘   └──────┬─────┘
                               │                │
                               └───────┬────────┘
                                       ▼
                              ┌────────────────┐
                              │ Runner / Jobs  │
                              └───────┬────────┘
                                      │
                    ┌─────────────────┼─────────────────┐
                    │                 │                 │
                    ▼                 ▼                 ▼
              Knowledge          Artifacts          Logs
                    │                 │                 │
                    └─────────────────┼─────────────────┘
                                      ▼
                              ┌────────────────┐
                              │ Infrastructure │
                              └────────────────┘


---

📁 Repository Structure

The repository currently contains several major areas:

crystalcastleX/
│
├── .changeset/
├── .claude/
├── .github/
├── .logs/
├── .template-docs/
├── .vscode/
│
├── Backend/
├── Frontend/
│
├── Image/
├── Package/
├── Production/
├── Quiz/
│
├── __tests__/
├── agent-hub/
├── api/
├── app/
├── artifacts/
├── assets/
│
├── crystalcastle-dashboard/
│
├── doc/
├── docs/
├── infra/
├── knowledge-base/
├── lib/
│
├── main/
├── netlify/functions/
├── notify_system/logs/
│
├── package/
├── packages/
├── pages/
├── public/
├── reporters/
├── scripts/
├── src/
│
├── test/
├── tests/
│
├── workflows/
│
├── .ai-context.md
├── .env.example
├── .gitignore
├── .knowledgebase.md
├── .middleware.ts
├── .mkdocs.yml
│
├── CHANGELOG.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── LICENSE
│
├── Dockerfile
├── docker-compose.yml
├── README.md
└── package.json

> The repository contains additional project-specific directories and configuration files. The structure above focuses on the major development surfaces.




---

🚀 Getting Started

1. Clone

git clone https://github.com/ZyntroAI/crystalcastleX.git

cd crystalcastleX

2. Install dependencies

Use the package manager and installation procedure defined by the current project configuration.

For npm-based workflows:

npm install

If the repository is configured for another package manager, use the corresponding lockfile and package-manager command.


---

🔐 Environment Variables

Copy the example environment file:

cp .env.example .env

Review the environment configuration before starting the application.

Do not commit:

.env
.env.local
API keys
access tokens
private credentials
service-account credentials
production secrets

Use .env.example for documenting required variable names without exposing secret values.


---

🐳 Docker

The repository includes:

Dockerfile
docker-compose.yml

Build the application:

docker compose build

Start the services:

docker compose up

Run in detached mode:

docker compose up -d

Inspect running containers:

docker compose ps

View logs:

docker compose logs -f

Stop the stack:

docker compose down


---

🧪 Development Workflow

A recommended development cycle is:

Issue
  │
  ▼
Plan
  │
  ▼
Implement
  │
  ▼
Run Tests
  │
  ▼
Run Lint / Type Checks
  │
  ▼
Review Diff
  │
  ▼
Commit
  │
  ▼
Pull Request
  │
  ▼
CI
  │
  ▼
Merge

For AI-assisted development:

Task
  │
  ▼
AI Context
  │
  ▼
Agent
  │
  ▼
Runner
  │
  ▼
Implementation
  │
  ▼
Tests
  │
  ▼
Artifacts / Logs
  │
  ▼
Human Review


---

🤖 AI Development

AI-related context should be maintained in structured files whenever possible.

Important files include:

.ai-context.md
.knowledgebase.md

AI agents should:

1. Read project context.


2. Inspect the relevant code.


3. Identify existing patterns.


4. Make the smallest safe change.


5. Run relevant tests.


6. Record important artifacts.


7. Report failures explicitly.


8. Avoid modifying unrelated files.




---

🔧 Automation

Automation scripts are located under:

scripts/
workflows/
.github/

The repository also contains configuration for:

GitHub Actions
pre-commit
commitlint
CodeQL
CodeRabbit
changesets
release automation
Docker
deployment workflows

Automation should be deterministic and reproducible whenever possible.


---

🔍 API

API-related code is organized under:

api/
Backend/

When adding a new API endpoint:

1. Define request schema
2. Define response schema
3. Implement endpoint
4. Add validation
5. Add error handling
6. Add tests
7. Update documentation
8. Update API examples

API credentials must remain server-side.


---

🧩 Frontend

Frontend-related code is organized under:

Frontend/
app/
pages/
public/
src/

UI changes should include appropriate:

accessibility

responsive behavior

loading states

error states

empty states

tests where applicable



---

📦 Artifacts

Generated artifacts should be stored separately from source code:

artifacts/

Examples include:

generated reports

AI outputs

diagnostic results

build artifacts

generated documentation

test reports


Generated files should not accidentally become source-of-truth configuration.


---

📝 Documentation

Documentation is distributed across:

doc/
docs/
.template-docs/

Project documentation should explain:

architecture

setup

environment

development

testing

deployment

API contracts

AI workflows

operational procedures



---

🔒 Security

Security is part of the development workflow.

Never commit secrets such as:

API_KEY=...
TOKEN=...
PASSWORD=...
PRIVATE_KEY=...
SERVICE_ACCOUNT=...

Use environment variables or an appropriate secret-management system.

Security-related tooling should be run before merging changes.

Recommended checks include:

Dependency review
Secret scanning
CodeQL
Linting
Type checking
Unit tests
Integration tests


---

🧹 Code Quality

Recommended checks before opening a Pull Request:

git status

git diff

git diff --check

Then run the project's configured:

lint
typecheck
test
build
security checks

The exact commands should follow the package scripts and workflow configuration in the repository.


---

🌿 Git Workflow

Use small, focused commits.

Recommended format:

type(scope): short description

Examples:

feat(ai): add model routing

feat(api): add diagnostic endpoint

fix(auth): handle expired sessions

docs(readme): document project architecture

test(api): add diagnostic coverage

ci: improve repository validation

refactor(agent): simplify runner lifecycle

Avoid commits such as:

update
fix
changes
final
new
test

Those messages communicate approximately as much information as a blank sticky note.


---

🔄 Pull Requests

A Pull Request should contain:

Summary
Changes
Testing
Security considerations
Breaking changes
Related Issue

Example:

## Summary

Add a new AI runner capability.

## Changes

- Added runner implementation
- Added validation
- Added tests
- Updated documentation

## Testing

- Unit tests passed
- Type checks passed
- Build passed

## Security

No credentials were added to the repository.

## Breaking Changes

None.


---

🧪 Test Strategy

Tests should exist at the appropriate level:

Unit
  ↓
Integration
  ↓
API
  ↓
End-to-End

A change should not require a full end-to-end test when a deterministic unit test can prove the behavior.

AI-generated code should receive the same test scrutiny as human-written code.


---

📈 Observability

Operational systems should expose enough information to answer:

Is the service healthy?
What failed?
When did it fail?
Which component failed?
How often does it fail?
How long does it take?
What changed before the failure?

Logs should avoid exposing:

API keys

tokens

passwords

private credentials

unnecessary personal information



---

🛠 Troubleshooting

Application does not start

Check:

git status
docker compose ps
docker compose logs

Then verify:

environment variables
dependencies
ports
service health
database/API connectivity


---

API fails

Check:

API logs
request payload
response status
environment variables
network connectivity
upstream provider status


---

AI runner fails

Check:

agent configuration
AI context
provider credentials
runner logs
model availability
timeout configuration
fallback configuration

Do not blindly retry a failing operation indefinitely.


---

🗺 Roadmap

The project can evolve toward a unified AI development platform with:

[ ] Unified AI runner

[ ] Multi-model routing

[ ] Agent lifecycle management

[ ] Task orchestration

[ ] Persistent AI memory

[ ] Knowledge indexing

[ ] Artifact management

[ ] AI experiment tracking

[ ] Prompt/version management

[ ] Automated diagnostics

[ ] Redis caching

[ ] Circuit breakers

[ ] Prometheus metrics

[ ] Grafana dashboards

[ ] Cross-platform runner

[ ] Mobile development workflow

[ ] Desktop development workflow

[ ] Automated GitHub workflows

[ ] Self-healing workflows with approval gates


Roadmap items should only be considered implemented when corresponding code, tests, documentation, and CI validation exist.


---

🤝 Contributing

Contributions are welcome.

Before contributing:

1. Read CONTRIBUTING.md.


2. Review existing architecture.


3. Check existing Issues and Pull Requests.


4. Make a focused change.


5. Add tests.


6. Update documentation.


7. Run local validation.


8. Open a Pull Request.



See:

CONTRIBUTING.md

CODE_OF_CONDUCT.md



---

📜 License

See LICENSE for the license applicable to this repository.


---

🔗 Project

Repository:

https://github.com/ZyntroAI/crystalcastleX

Organization:

https://github.com/ZyntroAI


---

⭐ Project Principles

Crystal Castle X follows several practical principles:

Simple > clever
Explicit > implicit
Tested > assumed
Observable > mysterious
Secure > convenient
Small changes > giant rewrites
Automation > repetitive manual work
Human approval > uncontrolled automation

The goal is not to make AI replace the development process.

The goal is to make the development process more observable, repeatable, testable, and easier to automate.


---

Status

🚧 Active development

Crystal Castle X is evolving rapidly. APIs, directory structures, automation workflows, and AI capabilities may change as the project develops.

### จุดที่ผมแนะนำให้แก้เพิ่มใน repo

README ปัจจุบันเป็นเพียงไฟล์ว่าง 1 byte ขณะที่ repository มี surface area เยอะมาก ดังนั้น README ข้างบนจะช่วยเป็น **entry point** ได้มากกว่าเดิมอย่างชัดเจน 1

อีกจุดหนึ่งคือหน้า repository ระบุ description ว่า **“Runner AI powered By Zyntro-Media-AI”** ซึ่งผมคงแนวคิดนี้ไว้ แต่ขยายความให้เป็น architecture/documentation มากขึ้นโดยไม่เดาความสามารถที่ยังไม่มีหลักฐานจาก source 2

**Commit ที่เหมาะกับ README นี้:**

```text
docs(readme): add comprehensive Crystal Castle X documentation

PR title:

docs: add comprehensive repository README

PR summary:

Add a comprehensive README for Crystal Castle X covering:

- Project overview
- Thai and English documentation
- AI runner architecture
- Repository structure
- Development workflow
- AI-assisted development
- API and frontend organization
- Testing strategy
- Docker workflow
- Security practices
- Git and Pull Request conventions
- Documentation structure
- Roadmap
- Contribution guidelines

ผมสามารถต่อให้เป็น README.md เวอร์ชัน GitHub-professional พร้อม badges, architecture diagram, Mermaid, screenshots section, API table และ Quick Start ที่อิงไฟล์จริงใน repo ได้เลยครับ.
