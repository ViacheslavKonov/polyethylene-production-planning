# Decisions to resolve with product owner

The functional specification explicitly leaves several topics for the technical design stage. These are **open questions**, not hidden assumptions.

| ID | Decision | Suggested default for prototyping, NOT a production constraint |
|---|---|---|
| ADR-001 | Real equipment topology, parallel lines, intermediate storages | Synthetic two-line reference model |
| ADR-002 | Optimization approach for annual grade wheels | Benchmark MILP/CP variants against simple heuristic |
| ADR-003 | Simulation engine / chemical fidelity and licensing | Plugin architecture, no chemical model in core |
| ADR-004 | Hard vs soft constraints and KPI weights | Explicit scenario presets and feasibility first |
| ADR-005 | Calendar week starts, shifts, time-zone and holiday calendars | Explicit plant-local calendar object; no silent ISO assumption |
| ADR-006 | Data feed contracts with MES/ERP/data warehouse | Versioned JSON contracts + mock adapter until agreed |
| ADR-007 | Access control, SSO provider, internet/intranet access | Localhost-only before approved identity provider |
| ADR-008 | Excel add-in delivery mechanism | API-first export; plugin separately after security design |
| ADR-009 | Solver choice, packaging, licenses and deployment constraints | No closed solver dependency in starter |
| ADR-010 | Release policy, migrations, HA, recovery requirements | 1 replica + manual approvals until proven |
| ADR-011 | Legal rights to publish requirements/code and open-source license | Public deidentified docs; no LICENSE yet |
| ADR-012 | Storage areas within scope and transfer boundary | Only factory silos / byproduct tanks, not external LC |

Every decision should be added as a separate ADR with rationale and tests when confirmed.
