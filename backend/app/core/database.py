from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from .config import settings
import logging

# Create database engine with improved connection management
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO,
    pool_pre_ping=True,
    pool_recycle=300,  # Recycle connections every 5 minutes
    pool_size=10,      # Base pool size
    max_overflow=20,   # Allow overflow connections
    pool_timeout=30    # Timeout for getting connection
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create declarative base
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logging.error(f"Database error: {e}")
        db.rollback()
        raise
    finally:
        try:
            db.close()
        except Exception as e:
            logging.error(f"Error closing database connection: {e}")

# Synchronous database operations
def get_sync_db() -> Session:
    return SessionLocal()

# Create database tables
def create_tables():
    try:
        Base.metadata.create_all(bind=engine)
        logging.info("Database tables created successfully")
    except Exception as e:
        logging.error(f"Error creating database tables: {e}")
        raise

# Drop database tables
def drop_tables():
    try:
        Base.metadata.drop_all(bind=engine)
        logging.info("Database tables dropped successfully")
    except Exception as e:
        logging.error(f"Error dropping database tables: {e}")
        raise
