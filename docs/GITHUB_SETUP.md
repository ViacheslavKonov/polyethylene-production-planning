# Publish the prepared code to a PUBLIC GitHub repository

The starter files are local until a new GitHub repository has been created. The GitHub connector used to prepare this starter can work with existing repositories but cannot create a repository with public/private visibility.

## Option A — GitHub CLI (shortest)

Install `git` and [`gh`](https://cli.github.com/), authenticate with `gh auth login`, unpack the provided ZIP, then from its root:

```bash
git init -b main
git add .
git commit -m "chore: bootstrap polyethylene production planning"
gh repo create ViacheslavKonov/polyethylene-production-planning --public --source=. --remote=origin --push
```

Choose an empty repo (no generated README), otherwise initial histories conflict. `gh repo create ... --public` is the action that **actually** creates the public repository. Do not execute unless ready to publish the included files.

## Option B — Browser + Git

1. Open https://github.com/new and create `polyethylene-production-planning` under `ViacheslavKonov`, visibility **Public**, without initializing README/.gitignore/license.
2. Unpack ZIP and run:

```bash
git init -b main
git add .
git commit -m "chore: bootstrap polyethylene production planning"
git remote add origin https://github.com/ViacheslavKonov/polyethylene-production-planning.git
git push -u origin main
```

3. Inspect the `CI` and `Publish container` Actions. First main branch push should publish the image, only after automated quality checks pass.
4. Check GHCR package visibility; a repo being public does not guarantee every registry package is world-readable.
5. In Codex, select that repository and use the `PE-001` task from `AGENTS.md`; create a feature branch/PR.
6. Deploy from Git in Portainer as described in [`PORTAINER.md`](PORTAINER.md).

**Do not upload the original functional specification DOCX or actual plant data to the new public repository.**
