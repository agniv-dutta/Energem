from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from backend.config import get_settings

settings = get_settings()

engine_kwargs = {"echo": False}
if settings.database_url.startswith("sqlite"):
    # Required for SQLite when used in FastAPI app contexts.
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(settings.database_url, **engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    from backend.db import models  # noqa: F401 - ensure table metadata is registered

    Base.metadata.create_all(bind=engine)
    _ensure_procurement_schema()
    _seed_corridors()


def _ensure_procurement_schema():
    inspector = inspect(engine)
    if "recommendations" in inspector.get_table_names():
        existing_columns = {column["name"] for column in inspector.get_columns("recommendations")}
        required_columns = {
            "supplier": "TEXT",
            "volume_bbl_per_day": "INTEGER",
            "eta_days": "INTEGER",
            "cost_premium_per_barrel": "FLOAT",
            "geopolitical_risk": "VARCHAR(20)",
            "confidence": "INTEGER",
            "reasoning": "TEXT",
            "status": "VARCHAR(30)",
            "approved_by": "VARCHAR(255)",
            "approved_at": "DATETIME",
        }
        with engine.begin() as connection:
            for column_name, column_type in required_columns.items():
                if column_name not in existing_columns:
                    connection.execute(text(f"ALTER TABLE recommendations ADD COLUMN {column_name} {column_type}"))

    if "authorization_log" not in inspector.get_table_names():
        Base.metadata.tables["authorization_log"].create(bind=engine, checkfirst=True)


def _seed_corridors():
    from backend.db.models import Corridor
    from backend.services.corridor_service import SEED_CORRIDORS

    inspector = inspect(engine)
    if "corridors" not in inspector.get_table_names():
        return
    session = SessionLocal()
    try:
        existing_ids = {row[0] for row in session.query(Corridor.corridor_id).all()}
        inserted = 0
        for data in SEED_CORRIDORS:
            if data["corridor_id"] not in existing_ids:
                session.add(Corridor(**data))
                inserted += 1
        if inserted:
            session.commit()
    except Exception:
        session.rollback()
    finally:
        session.close()
