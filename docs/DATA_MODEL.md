# Data model / API contract v0.1

## Existing persistent objects

- `Scenario`: UUID id, name, level (annual/tactical/operational), immutable validated JSON payload, UTC creation timestamp.
- `PlanRun`: UUID id, scenario UUID, engine identifier, immutable result JSON, UTC creation timestamp.

Data are retained until a future retention policy is established. This is not yet a versioned enterprise master-data system; a scenario is immutable after creation, and run results reference its input snapshot.

## Illustrative scenario payload

See [`examples/demo-scenario.json`](../examples/demo-scenario.json). Structure:

```json
{
  "name": "Synthetic demo",
  "level": "tactical",
  "data": {
    "grades": [{ "code": "PE_A", "feedstock_kg_per_ton": 1050 }],
    "buckets": [{ "label": "W1", "start": "2026-11-02", "end": "2026-11-08", "granularity": "week", "capacity_tons": 150, "demand_tons": {"PE_A": 120} }],
    "initial_inventory_tons": {"PE_A": 0},
    "changeover_loss_tons": 0
  }
}
```

Starter data semantics: one abstract production capacity per bucket; no parallel equipment, no supplier constraints, demand is assumed to be served at bucket end; coefficients only for **illustration** and not material-balance certified. `changeover_loss_tons` represents aggregate capacity consumed at change of produced grade. Loss and grade ordering are **not** industrial grade-wheel optimization.

## Existing API

| Method | Path | Description |
|---|---|---|
| GET | `/` | Web client |
| GET | `/api/health` | DB health/readiness |
| GET | `/api/meta` | API capabilities/limitations |
| GET | `/api/scenarios` | Scenario list |
| POST | `/api/scenarios` | Validate + create immutable scenario |
| GET | `/api/scenarios/{id}` | Scenario snapshot |
| POST | `/api/scenarios/{id}/runs` | Run illustrative baseline |
| GET | `/api/scenarios/{id}/runs` | Previous runs |
| GET | `/api/runs/{run_id}` | Run detail |

All endpoints are **unauthenticated** and must remain local-only until PE-006. No writes to equipment or external systems.

## Proposed normalized model

```text
Plant 1—N ProductionUnit 1—N Equipment
ProductionUnit N—M Grade [capability, nominal throughput]
Equipment 1—N AvailabilityInterval / MaintenanceWindow
Grade 1—N RecipeVersion 1—N MaterialUsage / ResourceUsage
Grade—Grade ChangeoverRule [affected equipment, duration, transitional volume]
StorageLocation [capacity, allowed grades, initial balance]
ProcessNode—ProcessEdge [material, constraints, yield]
InputDataset [version, source, checksum, imported_at, validation_status]
Scenario [dataset snapshot, config revision, parent scenario]
Plan [scenario, solver run, version, status, lock, approval]
PlanLine [bucket, grade, site/unit, release/readiness timestamps, quantity/unit]
Operation [unit, resource, start, end, grade, predecessor]
Run [queued/running/succeeded/failed, progress, objective, infeasibilities]
AuditEvent [actor, permission, object, before/after, timestamp]
```

Require explicit units and a calendar. For new persisted numeric quantities, move to SQL `NUMERIC` and Python `Decimal` as precision tolerances are agreed; float in the demo is not production quality. Avoid accidental inventory double counting across storage locations or horizons.
