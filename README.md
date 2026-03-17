# Finance

This repository is used to create access to the finance database using the following technology stack:

1. PostgresQL database
2. SQLAlchemy ORM (Python)
3. Pythong
4. Flask/Jinga (WSGI)

SQLAlchemy is used to abstract the physical database from the main application which is written in Python.   The models are exposed to the application via the models.py file.  

## Recreate finance_tst Schema Snapshot

Issue #34 requires creating a structural snapshot of schema `finance` into schema `finance_tst`.

Use the helper script:

```bash
chmod +x ./scripts/recreate_finance_tst_schema.sh
PGURI="postgresql+psycopg2://user:password@host:5432/finance" ./scripts/recreate_finance_tst_schema.sh --drop-existing
```

Notes:

- By default, source schema is `finance` and target schema is `finance_tst`.
- `--drop-existing` is optional but recommended for a clean re-create.
- The script clones schema objects (DDL) only; it does not copy table data.
