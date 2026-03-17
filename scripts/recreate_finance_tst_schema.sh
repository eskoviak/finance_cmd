#!/usr/bin/env bash
set -euo pipefail

# Clone the structure of schema "finance" into schema "finance_tst".
#
# Usage:
#   PGURI=<sqlalchemy-or-postgres-uri> ./scripts/recreate_finance_tst_schema.sh
#   PGURI=<uri> ./scripts/recreate_finance_tst_schema.sh --drop-existing
#   PGURI=<uri> ./scripts/recreate_finance_tst_schema.sh --source finance --target finance_tst

SOURCE_SCHEMA="finance"
TARGET_SCHEMA="finance_tst"
DROP_EXISTING=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --source)
      SOURCE_SCHEMA="$2"
      shift 2
      ;;
    --target)
      TARGET_SCHEMA="$2"
      shift 2
      ;;
    --drop-existing)
      DROP_EXISTING=true
      shift
      ;;
    -h|--help)
      cat <<'EOF'
Usage:
  PGURI=<uri> ./scripts/recreate_finance_tst_schema.sh [options]

Options:
  --source <schema>        Source schema name (default: finance)
  --target <schema>        Target schema name (default: finance_tst)
  --drop-existing          Drop target schema before recreation
  -h, --help               Show this help
EOF
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      exit 1
      ;;
  esac
done

if [[ -z "${PGURI:-}" ]]; then
  echo "PGURI is required (expected SQLAlchemy or libpq connection URI)." >&2
  exit 1
fi

if [[ "$SOURCE_SCHEMA" == "$TARGET_SCHEMA" ]]; then
  echo "Source and target schemas must be different." >&2
  exit 1
fi

# Convert common SQLAlchemy URI forms to libpq-compatible URIs for pg_dump/psql.
PGURI_PSQL="${PGURI/postgresql+psycopg2:/postgresql:}"
PGURI_PSQL="${PGURI_PSQL/postgresql+psycopg:/postgresql:}"

if ! command -v pg_dump >/dev/null 2>&1; then
  echo "pg_dump is required but was not found on PATH." >&2
  exit 1
fi

if ! command -v psql >/dev/null 2>&1; then
  echo "psql is required but was not found on PATH." >&2
  exit 1
fi

if [[ "$DROP_EXISTING" == "true" ]]; then
  psql "$PGURI_PSQL" -v ON_ERROR_STOP=1 \
    -c "DROP SCHEMA IF EXISTS ${TARGET_SCHEMA} CASCADE;"
fi

psql "$PGURI_PSQL" -v ON_ERROR_STOP=1 \
  -c "CREATE SCHEMA IF NOT EXISTS ${TARGET_SCHEMA};"

pg_dump "$PGURI_PSQL" \
  --schema="$SOURCE_SCHEMA" \
  --schema-only \
  --no-owner \
  --no-privileges \
| sed -e "s/SCHEMA ${SOURCE_SCHEMA}/SCHEMA ${TARGET_SCHEMA}/g" \
      -e "s/${SOURCE_SCHEMA}\./${TARGET_SCHEMA}./g" \
      -e "s/\"${SOURCE_SCHEMA}\"\.\"/\"${TARGET_SCHEMA}\".\"/g" \
      -e "s/SET search_path = ${SOURCE_SCHEMA},/SET search_path = ${TARGET_SCHEMA},/g" \
| psql "$PGURI_PSQL" -v ON_ERROR_STOP=1

echo "Schema snapshot complete: ${SOURCE_SCHEMA} -> ${TARGET_SCHEMA}"
