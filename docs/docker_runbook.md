# Docker Runbook

This runbook documents the current Docker workflow for MyFinance.

## Scope

- Run the Flask web app in Docker.
- Connect to PostgreSQL running on the host system.
- Keep reverse proxy, worker, and Redis as future enhancements.

## Prerequisites

- Docker Desktop running.
- PostgreSQL running on the host.
- A valid PostgreSQL user/password/database with privileges on schema `finance`.

## Files Used

- `docker-compose.yml`
- `Dockerfile`
- `.env.docker` (local, not committed)
- `.env.docker.example` (template)

## First-Time Setup

1. Create local Docker env file from template.

```bash
cp .env.docker.example .env.docker
```

2. Edit `.env.docker` and set `PGURI`.

Example:

```env
PGURI=postgresql+psycopg2://postgres:YOUR_PASSWORD@host.docker.internal:5432/finance
```

3. Build and start the app container.

```bash
docker compose up --build
```

4. Open the app.

```text
http://localhost:5010
```

## Normal Dev Cycle

1. Pull or change code on host.
2. Rebuild and restart app container.

```bash
docker compose up -d --build --force-recreate myfinance-web
```

3. Check logs.

```bash
docker compose logs -f myfinance-web
```

## Useful Commands

Start in detached mode:

```bash
docker compose up -d
```

Stop services:

```bash
docker compose down
```

Rebuild only web image:

```bash
docker compose build myfinance-web
```

Show resolved compose config:

```bash
docker compose config
```

## Troubleshooting

### App uses wrong database URI

Symptom:
- Log shows fallback URI or wrong password/database.

Checks:

```bash
docker compose config | grep -E "PGURI|env_file"
```

Fix:
- Ensure `.env.docker` exists.
- Ensure `.env.docker` contains `PGURI=...`.
- Recreate container:

```bash
docker compose up -d --build --force-recreate myfinance-web
```

### Permission denied for schema finance

Symptom:
- `psycopg2.errors.InsufficientPrivilege` against `finance.*` objects.

Typical SQL fix (run as schema owner or superuser):

```sql
GRANT USAGE ON SCHEMA finance TO postgres;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA finance TO postgres;
GRANT USAGE, SELECT, UPDATE ON ALL SEQUENCES IN SCHEMA finance TO postgres;
```

### Port 5010 already in use

Options:
- Stop the process already using 5010.
- Or map a different host port in `docker-compose.yml`.

## Notes

- `host.docker.internal` lets containers reach services running on the host machine.
- For now, PostgreSQL remains external to Docker by design.
