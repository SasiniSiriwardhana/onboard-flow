import logging
import time
from typing import Generator, Dict, Any
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError

from backend.config import settings

logger = logging.getLogger(__name__)

# Oracle SQLAlchemy Database URL
# Format: oracle+oracledb://system:mypassword@localhost:1521/?service_name=xe
DATABASE_URL = settings.sqlalchemy_database_url

# Create SQLAlchemy Engine
# Note: python-oracledb runs in Thin mode by default (pure Python, no Oracle Client binaries needed).
try:
    engine = create_engine(
        DATABASE_URL,
        pool_size=settings.DB_POOL_SIZE,
        max_overflow=settings.DB_MAX_OVERFLOW,
        pool_timeout=settings.DB_POOL_TIMEOUT,
        pool_pre_ping=True,  # Proactively test connection before usage
        echo=settings.DEBUG,
    )
except Exception as e:
    logger.error(f"Failed to initialize database engine: {e}")
    engine = None

# Session Factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Declarative Base for ORM Models
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that yields a SQLAlchemy database session per request
    and guarantees it is closed afterwards.
    """
    if SessionLocal is None:
        raise RuntimeError("Database session factory is not configured.")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_db_connection() -> Dict[str, Any]:
    """
    Diagnostic helper to test Oracle Database connectivity and measure ping latency.
    Safe to call in health checks; does not raise uncaught exceptions.
    """
    if engine is None:
        return {
            "status": "disconnected",
            "error": "Engine initialization failed",
            "host": settings.ORACLE_HOST,
            "port": settings.ORACLE_PORT,
            "service_name": settings.ORACLE_SERVICE_NAME,
        }

    start_time = time.time()
    try:
        with engine.connect() as connection:
            # Query standard Oracle dual table
            result = connection.execute(text("SELECT 1 FROM DUAL"))
            row = result.fetchone()
            latency_ms = round((time.time() - start_time) * 1000, 2)
            if row and row[0] == 1:
                return {
                    "status": "connected",
                    "driver": "python-oracledb (Thin Mode)",
                    "host": settings.ORACLE_HOST,
                    "port": settings.ORACLE_PORT,
                    "service_name": settings.ORACLE_SERVICE_NAME,
                    "user": settings.ORACLE_USER,
                    "latency_ms": latency_ms,
                }
    except SQLAlchemyError as err:
        return {
            "status": "disconnected",
            "host": settings.ORACLE_HOST,
            "port": settings.ORACLE_PORT,
            "service_name": settings.ORACLE_SERVICE_NAME,
            "error": str(err.orig if hasattr(err, "orig") else err),
            "latency_ms": round((time.time() - start_time) * 1000, 2),
            "hint": "Check if Oracle XE service is running on localhost:1521 or in Docker container.",
        }
    except Exception as exc:
        return {
            "status": "error",
            "error": str(exc),
            "host": settings.ORACLE_HOST,
            "port": settings.ORACLE_PORT,
            "service_name": settings.ORACLE_SERVICE_NAME,
        }

    return {"status": "unknown"}
