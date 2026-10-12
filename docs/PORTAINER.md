# Portainer deployment runbook

## Temporary prototype with direct browser access

For the explicitly requested development demo without an SSH tunnel, use
[`compose.prototype.yaml`](../compose.prototype.yaml), following
[`PROTOTYPE.md`](PROTOTYPE.md). It publishes HTTP on `0.0.0.0:8088` by default,
uses synthetic data, and has no application authentication or TLS.
The production stack described below has different access requirements.

## Prerequisites

- Linux Docker Engine + Portainer managing a Standalone Docker environment (Compose Stack); outbound access to GitHub and GHCR.
- Public GitHub repo with a successful `Publish container` GitHub Actions run on `main`.
- Available port, persistent storage for `pgdata`, operator able to restore DB dumps.
- Access restrictions: **do not** expose the app to the public internet until PE-006 authentication/RBAC and TLS termination are complete.

## First deployment

1. Under repository **Actions**, verify image `ghcr.io/viacheslavkonov/polyethylene-production-planning:main` exists. If GHCR reports unauthorized, check package visibility/permissions (package settings) or authenticate in Portainer Registry.
2. Portainer → target Docker environment → **Stacks → Add stack → Git repository**.
3. Repository URL: `https://github.com/ViacheslavKonov/polyethylene-production-planning`.
4. Repository reference: `refs/heads/main`; compose path: `compose.yaml`.
5. Enter environment variables (see `.env.example`):
   - `POSTGRES_DB=pe_planning`
   - `POSTGRES_USER=pe_planning`
   - `POSTGRES_PASSWORD=<your unique secret>`
   - `APP_IMAGE=ghcr.io/viacheslavkonov/polyethylene-production-planning:main`
   - `WEB_BIND_ADDRESS=127.0.0.1`
   - `WEB_PORT=8088`
6. Deploy and verify both `db` and `app` are healthy. `curl -fsS http://127.0.0.1:8088/api/health` on the Docker host. The UI stays host-local; use a controlled SSH tunnel or a separately configured authenticated reverse proxy for access.

Portainer GitOps can poll git for stack changes; **note that an image rebuilt with the same `:main` tag does not guarantee redeployment/pull**. For reproducible releases use immutable image tags/digests (or explicit image pull/redeploy). Do not enable unattended upgrades of persistent schema without a backup and rollback plan.

## Operational notes

- Database is on the private Compose network; no exposed DB host port.
- App runs as non-root and with read-only filesystem / `/tmp` tmpfs.
- App startup runs `alembic upgrade head` and MUST have one replica only.
- DB volume `pgdata` survives container recreation, but **not** `docker compose down -v`, volume deletion or host loss.
- Reverse proxy should terminate HTTPS, restrict access, and provide trustworthy upstream metadata; the current application has no authentication or CSRF protection and is not ready for even internal multi-user production use.
- Back up both PostgreSQL data **and uploaded source files** when dataset uploads are implemented; current release has no file uploads.

## Manual backup / restore (development illustration)

`docker exec` container IDs depend on Portainer Stack names, therefore use the Portainer console or identify running DB container. Use an operator-controlled path on the host.

```bash
# Example: substitute actual DB container id, never commit credentials/dumps.
docker exec -e PGPASSWORD="$POSTGRES_PASSWORD" <db-container> \
  pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc > backup.dump

# Restore only into an isolated prepared replacement database; never overwrite live DB.
cat backup.dump | docker exec -i -e PGPASSWORD="$POSTGRES_PASSWORD" <new-db-container> \
  pg_restore -U "$POSTGRES_USER" -d "$POSTGRES_DB" --no-owner
```

This is a **manual example**, not a compliant backup policy. Required by the functional brief: recover within 1 h (RTO); max data loss 24 h for volume plans, 4 h for operational scheduling (RPO). These targets require monitoring, periodic backups and timed restore exercises and are **not yet met**.

## Local smoke test

```bash
docker compose -f compose.dev.yaml config
docker compose -f compose.dev.yaml up -d --build
curl -fsS http://127.0.0.1:8088/api/health
```
