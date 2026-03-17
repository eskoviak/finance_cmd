import os

from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base


def get_model_schema() -> str:
    """Return schema for ORM metadata based on environment.

    Priority:
    1) MYFINANCE_DB_SCHEMA override when explicitly provided.
    2) finance_tst when running in test/testing env.
    3) finance for all other environments.
    """
    schema_override = os.getenv("MYFINANCE_DB_SCHEMA")
    if schema_override:
        return schema_override

    flask_env = (os.getenv("FLASK_ENV") or os.getenv("FLASH_ENV") or "").strip().lower()
    if flask_env in {"test", "testing"}:
        return "finance_tst"

    return "finance"


Base = declarative_base(metadata=MetaData(schema=get_model_schema()))
