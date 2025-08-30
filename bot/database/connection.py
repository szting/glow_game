import os
from sqlalchemy import create_engine as sa_create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from typing import Optional
from ..config import get_settings

settings = get_settings()

def get_database_url() -> str:
    """Get database URL from environment variables"""
    if settings.database_url:
        return settings.database_url
    
    # Fallback to SQLite for development
    return "sqlite:///./rainbow_bot.db"

def create_engine():
    """Create database engine with appropriate configuration"""
    database_url = get_database_url()
    
    if database_url.startswith("sqlite"):
        # SQLite configuration for development
        return sa_create_engine(
            database_url,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
            echo=settings.debug
        )
    else:
        # PostgreSQL configuration for production
        return sa_create_engine(
            database_url,
            pool_pre_ping=True,
            pool_recycle=300,
            echo=settings.debug
        )

# Create engine instance
engine = create_engine()

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_session() -> Session:
    """Get database session"""
    return SessionLocal()

def get_db():
    """Dependency for FastAPI to get database session"""
    db = get_session()
    try:
        yield db
    finally:
        db.close()
