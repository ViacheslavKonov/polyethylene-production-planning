# Instructions for Codex contributors

You are working on **polyethylene production planning**: annual volume planning, tactical volume-calendar planning, and operational daily/weekly scheduling. See `docs/REQUIREMENTS.md` for the scope and original `[фпNNN]` requirement references.

## Top priority

Implement the next incomplete `PE-xxx` work item from `docs/WORK_ITEMS.md`, beginning with **PE-001**. One coherent PR per vertical slice. Do not replace the starter with an unrelated boilerplate.

## Truthfulness and safety rules

1. This is **not** a working industrial optimizer. The current engine in `app/planning.py` is an explicitly labelled, illustrative heuristic. Never describe baseline output as optimal or technologically feasible.
2. Never import production datasets, corporate names, internal integration addresses, secrets, or the private DOCX specification into this public repository. Synthetic fixtures only.
3. No application may control equipment or issue automatic operations to MES/ERP. Integrations are data exchange only, with approval and audit requirements.
4. Respect the boundary: planning only up to transfer of finished product to the logistics complex; detailed warehouse logistics and external transport planning are excluded.
5. Store and compute physical quantities with **explicit units**. Dates in UTC for audit and location-specific calendar/bucket semantics for planning. Do not silently coerce quantities or invent plant parameters.
6. Protect hard constraints (capacity, maintenance, storage, grade wheels) and report infeasible cases; soft constraints must be quantified transparently.
7. The app does **not yet have authentication**. Keep published compose bound to `127.0.0.1`, DB on internal network, never enable public exposure as part of a feature without completed authorization, audit, session and TLS requirements.

## Technology and design

- Python 3.12 / FastAPI / Pydantic 2 / SQLAlchemy 2 / PostgreSQL 16 / Alembic.
- Minimal static TypeScript-free UI at present; API-first, domain logic independent of HTTP and storage.
- Portainer deployment from `compose.yaml` and a prebuilt GHCR image; `compose.dev.yaml` builds locally.
- Implement solvers through a versioned adapter (`PlanningEngine` protocol), not inline endpoints. Design for OR-Tools/HiGHS adapters and longer-running async jobs but do not claim they exist until delivered.
- For production functions, add explicit contracts, schema migrations, validation and tests; keep generated plans immutable. Never overwrite approved plans silently.

## Required checks for every PR

```bash
python -m pip install -e '.[dev]'
pytest -q
ruff check .
```

For Docker or Compose changes, also check `docker compose -f compose.dev.yaml config` and build/run smoke test when Docker is available. Document untested steps honestly when unavailable.

## Working agreement

- Update `docs/REQUIREMENTS.md` traceability and `docs/WORK_ITEMS.md` status for each implemented requirement group.
- Include tests for correct path, boundary conditions, infeasible constraints, duplicate/malformed data, and authorization where applicable.
- New API operations: OpenAPI schemas, actionable errors, pagination where needed, reliable audit trail, migration for persisted data.
- Prepare deterministic synthetic fixtures, never real values. Do not sneak in undocumented performance claims.
- Keep changes compatible with the Portainer stack or explicitly provide migration instructions.

## First task prompt

> Implement `PE-001` as defined in `docs/WORK_ITEMS.md`: model plants/units/equipment/grades/silos/resources, links/availability/calendar/grade transition matrix with migrations, synthetic fixture, validation, REST CRUD and integration tests. Keep the existing baseline demo working; add explicit capacity ownership to avoid double counting. Open a PR and list supported requirement IDs. Do not attempt to call the result an optimizer.
