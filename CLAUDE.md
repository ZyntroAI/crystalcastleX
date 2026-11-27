#CrystalCastle X Engineering Standards This document defines mandatory rules for all AI agents and contributors. Failure to follow these rules is considered a defect. --- # Architecture ## Backend Stack: - Python 3.12+ - FastAPI - Pydantic v2 - SQLAlchemy 2.x - PostgreSQL - Redis Requirements: - Async-first - Type-safe - Dependency Injection - Repository Pattern Avoid: - Global mutable state - Circular imports - Raw SQL unless justified --- ## Frontend Stack: - React - TypeScript - Vite - TanStack Query Requirements: - Strict TypeScript - Component composition - Feature-based structure --- # Coding Standards ## Python Required: - Type hints - Docstrings for public APIs - Ruff compliance Example: ```python async def get_user( user_id: UUID, ) -> User: ...

Forbidden:

❌ Any

❌ print()

❌ Bare except

TypeScript

Required:

Strict mode enabled

Explicit return types on public functions

Forbidden:

❌ any

❌ ts-ignore

Testing Standards

Every feature requires tests.

Required:

✅ Unit Tests

✅ Integration Tests

✅ Regression Tests

Critical APIs require:

✅ k6 Load Tests

User-facing features require:

✅ Playwright Tests

Coverage:

Minimum:

80%

Target:

90%

Pull Requests failing coverage checks must not be merged.

k6 Standards

Critical APIs:

Login

Refresh Token

Search

Create Resource

Update Resource

Required:

P95 < 500ms

P99 < 1000ms

Error Rate < 1%

All load tests must include setup and teardown.

Test-created data must be deleted.

Security

Required:

JWT Authentication

RBAC

Secret Management

Dependency Scanning

Forbidden:

❌ Hardcoded Secrets

❌ Plaintext Passwords

❌ Secrets in Logs

Use:

Environment Variables

GitHub Secrets

Secret Managers

Database

Migrations:

Alembic required.

Every migration must support:

Upgrade

Downgrade

Forbidden:

❌ Irreversible migrations

Required:

✅ Index review

✅ Query review

✅ Foreign key validation

Observability

Required:

OpenTelemetry

Prometheus

Grafana

Structured Logging

Every request must include:

request_id

trace_id

span_id

Logs must be JSON.

Forbidden:

❌ print()

❌ unstructured logs

OpenTelemetry

Export Protocol:

OTLP

Required Metadata:

service.name

environment

service.version

git.commit.sha

Critical workflows require spans:

Login

Search

Create Resource

Background Jobs

Health Checks

Every service must expose:

GET /health

GET /ready

Docker:

healthcheck required

Kubernetes:

startupProbe required

readinessProbe required

livenessProbe required

CI/CD

Required Workflows:

ci.yml

security.yml

performance.yml

deploy-staging.yml

deploy-production.yml

GitHub Actions Gates

Merge blocked if:

❌ Lint fails

❌ Typecheck fails

❌ Unit Tests fail

❌ Integration Tests fail

❌ Playwright fails

❌ k6 fails

❌ Security Scan fails

❌ Coverage falls below 80%

Release Gates

Required:

✅ Tests Passed

✅ Security Passed

✅ Coverage Passed

✅ k6 Passed

✅ Observability Verified

✅ Rollback Verified

✅ Documentation Updated

Deployment

Deployment Method:

Helm

Required:

--atomic

--wait

Rollback Support:

Mandatory

Automatic Rollback

Trigger rollback when:

Health checks fail

Smoke tests fail

Error rate exceeds thresholds

Rollout times out

Rollback must be automatic.

SLO

Availability:

99.9%

Latency:

Read APIs

P95 < 500ms

P99 < 1000ms

Error Rate:

< 1%

Error Budget

Monthly Availability Goal:

99.9%

Allowed Downtime:

43m 49s

Policy:

<50% Normal development

50%-75% Increase monitoring

75%-100% Limit feature releases

100% Feature freeze

Reliability work only.

Cleanup Endpoints

Allowed Environments:

✅ local

✅ dev

✅ test

✅ staging

Forbidden:

❌ production

Requirements:

Authentication

Cleanup Token

Audit Logging

Rate Limiting

Distributed Locking

Documentation

Update documentation when:

API changes

Database changes

Infrastructure changes

Authentication changes

Required:

README

API Documentation

ADR

AI Agent Rules

When implementing features:

Add Types

Add Tests

Add Metrics

Add Traces

Add Logs

Add Documentation

Add Rollback Path

Add Cleanup Logic

Review Performance

Review Security

Feature complete means:

✅ Implemented

✅ Tested

✅ Observable

✅ Secure

✅ Deployable

✅ Recoverable

✅ Documented

Anything less is incomplete.

--- ## Why this works well ### Rule-based instead of Prompt-based แทนที่จะสั่งทุกครั้งว่า: ```text เพิ่ม test ด้วย เพิ่ม telemetry ด้วย เพิ่ม docs ด้วย

คุณเขียนไว้ใน CLAUDE.md ครั้งเดียว:

Every feature requires: - Tests - Metrics - Traces - Documentation

จากนั้น Claude Code จะพยายามทำตามทุก task ใน repo นั้น

Example Request

หลังมี CLAUDE.md นี้อยู่แล้ว คุณสามารถสั่งแค่:

Implement password reset flow.

Claude จะมีแนวโน้มทำเพิ่มให้เอง เช่น

✅ FastAPI endpoint ✅ Database migration ✅ Unit tests ✅ Integration tests ✅ OpenTelemetry spans ✅ Prometheus metrics ✅ API documentation ✅ GitHub Actions compatibility ✅ Rollback consideration

โดยไม่ต้องระบุรายการซ้ำทุกครั้ง

นี่คือแนวคิดที่ทีม Platform Engineering หลายทีมใช้จริง: ให้ CLAUDE.md เป็น "Engineering Constitution" ของโปรเจกต์ แล้วปล่อยให้ Claude Code ทำงานภายใต้กฎนั้นเสมอ.

