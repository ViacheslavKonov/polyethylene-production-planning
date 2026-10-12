# Functional requirements: public implementation brief

**Origin:** owner-provided Russian functional specification (45 pages). This is a **paraphrased engineering trace**, not the corporate source file. Identifiers `[фпNNN]` are preserved to connect code and tests to source requirements. Any ambiguities below remain unresolved design questions, not assumptions about actual plant operations.

## Objectives and levels

Three coupled horizons require a visible cascade from approved higher-level plans to detailed schedules: **annual volume** up to 18 months with monthly buckets, **tactical/volume-calendar** up to 3 months with weekly buckets, and **operational** up to 4 weeks with daily buckets. Telescopic bucket configurations may mix weekly/monthly or daily/weekly periods within the specified horizon. Produced volumes are accounted for by *product readiness / line output date* `[фп149–155, фп267, фп377–380, фп455]`.

Production is planned by physical quantities only; economic/cost optimization is **not specified** `[фп43]`. The scope includes polyethylene and identified byproducts, raw ethane/propane fractions, chemicals/materials, water, air, nitrogen, internal plant silos and byproduct tanks. **Electric power, steam, heat and fuel gas** are outside the resource planning perimeter, as is detailed logistics complex planning and external warehousing `[фп17, фп22, фп25, фп42–45, фп61–62, фп68]`.

## Requirements matrix

| ID / source | Capability | Acceptance evidence | Status |
|---|---|---|---|
| PE-D01 `[фп127–148, фп346–376]` | Imported/validated/versioned source datasets, dictionaries, archives and import reports; scheduled/manual load | CRUD/version history, validation report, import lineage | **Scaffold only** |
| PE-D02 `[фп205–229, фп552–605]` | Editable production + technological model, process graph, capacities, flows, routes, parameters and restrictions | Domain graph UI + data model, round-trip edit/version tests | Not implemented |
| PE-V01 `[фп149–180]` | Annual volume and tactical volume-calendar plans (materials, product, byproduct, resources and stocks) | Plans by scope/horizon/physical units | Baseline subset only |
| PE-V02 `[фп181–204]` | Different input datasets by horizon: distribution, supplies, repairs, availability and inventories | Snapshot datasets, integrity checks, import reports | Not implemented |
| PE-V03 `[фп230–249]` | Configurable optimizer parameters, weighted KPIs, hard and soft constraints, saved presets | Deterministic validation, persistence, infeasibility explanation | Not implemented |
| PE-V04 `[фп250–278]` | Many scenario versions, reproducible experiments, annual grade-wheel optimization, KPI comparisons, master/approved plan publication | Solver tests, run lineage, compare/approve/export | Only saved scenario + demo run |
| PE-V05 `[фп279–292]` | Replanning with fresh actuals, locked values and revision links | Versioned changes with frozen parameters | Not implemented |
| PE-V06 `[фп293–316]` | Material/byproduct/water-air-nitrogen calculations and shortage/surplus | Explicit balance formula test suite | Demo coefficients only |
| PE-S01 `[фп329–341, фп377–415]` | Operational schedules for individual units, raw inputs, repair schedules and grade operations | 28-day operational schedule with hard constraints | Not implemented |
| PE-S02 `[фп416–463]` | Configurable optimization/simulation algorithms, scenarios, KPI and schedule comparison | Deterministic benchmark; alternative schedules and explanation | Not implemented |
| PE-S03 `[фп464–500]` | Operational replanning, byproducts/material/energy balances | Actual-state replanning tests | Not implemented |
| PE-S04 `[фп502–538]` | Aggregate-specific operation schedule, resources, chemical supply and byproduct readiness | Resource-feasible Gantt/timeline | Not implemented |
| PE-I01 `[фп144–146, фп363–365]`, §3.4, §4.4 | Exchange with ERP/MES/data store/master data/distribution/warehouse | Versioned adapters with retries/idempotency and audit | Not implemented |
| PE-U01 `[фп123–126, фп343–345, фп608–615]` | RU/EN navigation, filters/search, role-aware screens, Excel integration, cascade visualizations | UX e2e and accessibility checks | RU demonstration only |
| PE-N01 `[фп616–647]` | 30 users, 80% UI interactions within 2 s, 24×7, RTO 1 h; RPO volume 24 h/scheduling 4 h | Load tests, backups + timed restore exercise | Deployment scaffold only |
| PE-SEC01 `[фп653–694, фп695–794]` | AuthN/AuthZ, single-session, secure audit, SIEM, integrity, password policies, compliance tests | Security assurance reports and audit evidence | **Not implemented** |

## Main business objects

`ProductionModel`, `TechnologyModel`, `Plant`, `ProductionUnit`, `Equipment`, `StorageLocation`, `Product`, `Grade`, `Recipe/BOM`, `MaterialFlow`, `Resource`, `MaintenanceWindow`, `Changeover`, `GradeWheel`, `InputDataset`, `Scenario`, `OptimizationConfig`, `Plan`, `Schedule`, `Run`, `KPI`, `Approval`, `AuditEvent`, `IntegrationJob`.

Current schema only includes `Scenario` and `PlanRun`; these other types are **domain targets**, not existing tables.

## Special constraints and exclusions

- Annual volume planning **optimizes grade-wheel sequences**, while tactical optimization takes approved wheels as hard input `[фп272]`; operational scheduling must respect inherited restrictions.
- Separate **hard** constraints (equipment/storage capacities, wheel length, safety rules) from **soft** targets (inventory targets, preferences) `[фп31–33, фп245–246, фп437–438]`.
- Configurable physical objective functions: maximize production/coverage/utilization, minimize downtime/changeovers; no inferred profit objective `[фп67, фп242–244]`.
- Approval and publication of plans **inside planning software**; corporate S&OP committee process and distribution-planning calculation are **external** `[фп54, фп277]`.
- Calendar granularity, time-zone rules and production readiness must be precisely modeled; use explicit period intervals `[фп267, фп345, фп455]`.
- Dynamic import from enterprise systems is deferred until real interfaces are agreed. Use dummy adapter fixtures only.

## Validation approach

For each requirement group require: domain/API contract; traceable test cases; expected valid & invalid scenarios; quantitative KPI calculations; migration/revision rules; security/privacy assertions; UI confirmation where relevant. **No unsupported feature may be marked complete.**
