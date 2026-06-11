import time
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from app.core.config import settings

engine_primary = create_engine(
    settings.DATABASE_URL,
    poolclass=NullPool,
    connect_args={"connect_timeout": 10},
)

engine_replica = create_engine(
    settings.DATABASE_URL_REPLICA,
    poolclass=NullPool,
    connect_args={"connect_timeout": 10},
)

SessionPrimary = sessionmaker(autocommit=False, autoflush=False, bind=engine_primary)
SessionReplica = sessionmaker(autocommit=False, autoflush=False, bind=engine_replica)

Base = declarative_base()


def get_db():
    # Escrituras siempre al primario; hasta 3 intentos por cold-start de Neon
    for attempt in range(3):
        db = SessionPrimary()
        try:
            db.execute(text("SELECT 1"))
            break
        except OperationalError:
            db.close()
            if attempt < 2:
                time.sleep(2)
            else:
                raise
    try:
        yield db
    finally:
        db.close()


def _connect_read():
    # Intenta réplica primero; si falla, cae al primario (availability pattern)
    labels = [(SessionReplica, "REPLICA"), (SessionPrimary, "PRIMARY (fallback)")]
    for SessionFactory, label in labels:
        db = SessionFactory()
        try:
            db.execute(text("SELECT 1"))
            print(f"[DB] read routed to {label}", flush=True)
            return db
        except OperationalError as e:
            print(f"[DB] {label} unavailable: {e}", flush=True)
            db.close()
    raise RuntimeError("All databases unavailable")


def get_db_read():
    db = _connect_read()
    try:
        yield db
    finally:
        db.close()
