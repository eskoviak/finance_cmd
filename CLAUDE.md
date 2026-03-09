# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MyFinance is a Flask-based financial management web application for managing vouchers, payables, liabilities, vendors, and accounts. It uses PostgreSQL as the database backend with SQLAlchemy 2.0 ORM.

## Development Commands

**Run the application:**
```bash
flask --app MyFinance.finance --debug run
```
Or use `./start.sh`. The app runs on port 5010 by default.

**Run tests:**
```bash
python -m unittest test.test_pg_utils
```

**Run a single test:**
```bash
python -m unittest test.test_pg_utils.TestPGUtils.test_get_voucher
```

**Build documentation:**
```bash
cd doc_src && make html
```

## Architecture

### Application Structure

- **`MyFinance/finance.py`** - Flask application factory. Creates the app, configures the PostgreSQL connection via `PGURI` environment variable, and registers all blueprints.

- **Blueprints** - Feature-based routing modules:
  - `auth.py` - User authentication (login, registration, session management)
  - `voucher.py` - Financial voucher entry and display
  - `payable.py` - Accounts payable management
  - `liability.py` - Loan/liability tracking
  - `search.py` - Search functionality
  - `register.py` - Register operations

### Data Layer

- **`MyFinance/utils/pg_utils.py`** - `PgUtils` class encapsulates all database operations. Methods return dictionaries for JSON serialization. This is the primary interface between blueprints and the database.

- **`MyFinance/models/`** - SQLAlchemy ORM models, all using `schema='finance'` on PostgreSQL:
  - `vouchers.py` - Voucher, VoucherDetail, VoucherType
  - `payables.py` - AccountsPayable, Liabilities, Periods
  - `entities.py` - ExternalAccounts, Company, CoA, PaymentType
  - `vendors.py` - Vendor
  - `user.py` - User

### Templates

Jinja2 templates in `MyFinance/templates/` are organized by feature (auth/, voucher/, payable/, liability/, search/, register/). All extend `base.html`.

## Configuration

- **`.flaskenv`** - Flask environment variables (app module, port, debug mode)
- **`.env`** - Contains `PGURI` connection string for PostgreSQL (not in git)

## Tech Stack

- Python 3.14
- Flask 2.3.2 with Jinja2 templating
- SQLAlchemy 2.0 with psycopg2-binary driver
- PostgreSQL 16
