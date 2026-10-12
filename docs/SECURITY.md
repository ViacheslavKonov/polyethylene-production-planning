# Security posture — NOT APPROVED FOR PRODUCTION

This publicly available starter contains **no login, no RBAC, no audit enforcement, no SIEM, no TLS service, no secure multi-user session controls and no independent security assessment**. Do not connect it to production ERP/MES or place it on an untrusted network.

## Current mitigations

- Portainer `compose.yaml` maps app port to host **127.0.0.1** by default; DB has no host port.
- No sensitive corporate input data, passwords or original business document in Git.
- Production Compose mandates a caller-supplied database password; non-root runtime; minimal filesystem writes; no host socket mounts.
- All examples are synthetic. Values are illustrative, not process recommendations.
- Basic request schema validation and DB health check.

## Required before any external/internal-user release

1. Authentication/SSO, enforced authorization on every HTTP route and object, role separation, audit log, configurable session lifetime and failed-login limits.
2. TLS termination, trusted reverse proxy, CSRF/CORS controls, request rate limits, upload protections, HTTP security headers.
3. Secrets manager/Portainer secrets where supported, secure DB credentials and rotation. Audit must never contain passwords.
4. Immutable provenance for scenarios/runs, approval controls, separation of administrator actions from production planning.
5. CI dependency/container scanning, SBOM, patch release process, database backup encryption and restore testing.
6. Threat model and formal evidence for any applicable regulatory requirements; do not claim certification or legal compliance based solely on this project.
7. SIEM event schema, audit retention/access controls, system integrity monitoring, asset/port inventory and minimal network pathways.

## Protection of source materials

Only public architectural paraphrases are stored here. Never commit an original corporate specification, customer/partner names, process values, credentials, personnel records, licensed vendor models or company-internal documentation. If a file accidentally enters Git history, rotating/deleting secrets and history remediation are required; editing a HEAD commit is insufficient.

The source requirements reference security standards and Russian legal acts; this repository provides **no certification**, and applicable law / exact deployment environment must be reviewed by responsible security specialists.
