# Codex work queue (implementation backlog)

Status: **PE-000 complete (scaffold only)**. Subsequent items are **not started**. Every PR must update the requirements matrix and tests; avoid creating placeholder endpoints that return fake optimized results.

## PE-001 — Production master-data model and migrations **START HERE**

**Goal:** model plant topology, units/equipment, storage, grades, production routes and grade transitions.

**Scope:** SQLAlchemy tables + Alembic upgrade; synthetic seed; CRUD with validation; test edge cases; no vendor-specific manufacturing values. Add plant/line/equipment, capabilities and capacities, maintenance calendars, grade recipe/material/resource norms, silos/storage restrictions and transition matrix. Model aggregation ownership to avoid summing shared line/equipment capacity twice.

**Acceptance:** deterministic fixture can be created via API; uniqueness and FK constraints work; invalid grades/routes/storage are rejected; schema migrated from scratch and test rollback/upgrade; current simple scenario page and API still work. Requirements: PE-D02, `[фп206–229]`, `[фп552–605]`.

## PE-002 — Dataset intake, validation, lineage and revisions

**Dependencies:** PE-001. **Scope:** normalized `InputDataset` + immutable versions, CSV/JSON upload (safe size limits), checked mappings, configurable validation rules, import report (source, version, timestamp, issues by path), deduplication by digest. Later adapters for ERP/MES are stubs with mock fixtures and documented contracts only.

**Acceptance:** rejects negative quantities, unknown refs, inconsistent dates, duplicate deliveries, material-balance mismatch; preserves original immutable dataset and issue report; unit tests. Requirements: PE-D01, PE-V02, `[фп367–376]`.

## PE-003 — Actual annual/tactical optimization engine

**Dependencies:** PE-001, PE-002. **Scope:** `PlanningEngine` protocol; separate model construction, solver adapter and result validator; hard/soft constraints; scenario parameter presets; objective weights; material availability, maintenance, capacity and internal silos; annual grade-wheel optimization and tactical use of fixed wheel; KPIs and infeasibility diagnostics.

**Acceptance:** deterministic synthetic feasibility/infeasibility benchmarks; no hard constraints violated; changing soft penalties changes ranking; solver version + gap/time-limit captured; fallback status declared, never labelled optimal if not proven. Requirements PE-V01–PE-V04 and PE-V06.

## PE-004 — Operational scheduler and telescopic calendar

**Dependencies:** PE-001–003. **Scope:** 28-day detailed operation/equipment schedule, dependencies, repair downtimes, setup times, day/week buckets, resource-by-period material balances, dates start ↔ product-ready.

**Acceptance:** no schedule overlap on exclusive equipment, no output before setup/end time, no negative silo inventory, explicit daily unit test cases and schedule visual. Requirements PE-S01–PE-S04.

## PE-005 — Compare, replan, freeze, approve, publish

**Dependencies:** PE-003–004. **Scope:** compare scenarios, KPI deltas, freezing selected periods/parameters, manual approval state machine, approved plan snapshots, audit, export API and downstream adapters (stub/mock until agreed).

**Acceptance:** only permitted approvers can approve; immutable approval record; replan respects freeze; historical plan preserved; failed export retries idempotently. Requirements PE-V04–PE-V05, PE-S02–PE-S03.

## PE-006 — Security and roles BEFORE external access

**Dependencies:** PE-001. **Scope:** user identity/SSO integration or locally hardened auth, admin vs planner vs analyst roles, per-route authorization, session lifecycle, audit, brute force defense, secret handling, controlled exports. Add safe TLS reverse proxy recipes and an explicit way to block network exposure on misconfiguration.

**Acceptance:** unauthorized API writes blocked; admins cannot casually perform business planning under admin accounts; no passwords in logs; comprehensive role tests; reviewed threat model. No internet-facing installation before completion. Requirements PE-U01, PE-SEC01.

## PE-007 — UI: production graph, plan cascade, Gantt, RU/EN

**Dependencies:** PE-001–006 as needed. **Scope:** UX design, responsive RU/EN, equipment/process graph editor, master-data grid, import reports, scenario KPI comparison, constraints/infeasibility visual, weekly/day Gantt, plan level drill-through; Excel plug-in assessed as separate workstream.

**Acceptance:** workflow tests with realistic synthetic fixture, visible disabled reasons, keyboard support. Requirements PE-U01.

## PE-008 — Backups, observability, performance and GitOps release

**Dependencies:** PE-003, PE-006. **Scope:** tested backup/restore, RPO targets (volume 24 h, operational 4 h) and RTO 1 h, metrics, correlated logs, SIEM forwarding contract, load testing for 30 active operational users, image vulnerability scan and SBOM, tagged releases and rollback strategy.

**Acceptance:** documented recovery exercise, p80 of UI requests under 2 s on agreed hardware for benchmark, restored Postgres consistency, audited change workflow. Requirements PE-N01, PE-SEC01.

## PE-009 — Real data integrations (only after interface contracts)

**Dependencies:** PE-002, PE-006. **Scope:** adapters to approved master-data, ERP, MES, data storage, distribution plan and warehouse; clear schema & endpoints, reconcile/approve, no direct industrial actuator or PLC control.

**Acceptance:** contract/integration tests with mock server, failure reconciliation, idempotency, sensitive-data controls. Requirements PE-I01.

## Definition of done

- Working code + migration + negative and positive tests; no fake outputs marked as finished.
- Document new API and parameter units, source IDs, security impact and Portainer compatibility.
- CI green and synthetic benchmark produced; clear issue/PR changelog and product owner decisions separated from code assumptions.
