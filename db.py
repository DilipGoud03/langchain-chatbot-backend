from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from decouple import config
import os
from dotenv import load_dotenv

# ------------------------------------------------------------
# Database Configuration and Initialization
# Description:
#   This module sets up SQLAlchemy with connection pooling,
#   scoped sessions, and declarative base for ORM models.
#
#   It loads environment variables from the `.env` file and
#   establishes a persistent database engine connection.
# ------------------------------------------------------------

# Load environment variables from .env
load_dotenv()


# ------------------------------------------------------------
# Database URL Construction
# ------------------------------------------------------------
# Combines credentials and host details to form the SQLAlchemy
# connection string dynamically from environment variables.
# Example:
#   mysql+pymysql://user:password@localhost:3306/mydatabase
# ------------------------------------------------------------
SQLALCHEMY_DATABASE_URL = "{}://{}:{}@{}:{}/{}".format(
    config("DB_ENGINE"),
    config("MYSQL_USER"),
    config("MYSQL_PASSWORD"),
    config("MYSQL_URL"),
    config("MYSQL_PORT"),
    config("MYSQL_DB"),
)


# ------------------------------------------------------------
# SQLAlchemy Engine
# ------------------------------------------------------------
# The engine manages the database connection pool and executes SQL.
# - pool_size: Maximum number of connections in the pool
# - pool_pre_ping: Validates connections before using them
# - isolation_level: Controls transaction isolation
# ------------------------------------------------------------
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=5,
    pool_pre_ping=True,
    isolation_level="READ COMMITTED",
)


# ------------------------------------------------------------
# Session Management
# ------------------------------------------------------------
# SessionLocal provides a factory for session instances bound
# to the configured engine. Scoped sessions ensure thread safety.
# ------------------------------------------------------------
SessionLocal = sessionmaker(bind=engine)
SessionLocal = scoped_session(SessionLocal)


# ------------------------------------------------------------
# Declarative Base
# ------------------------------------------------------------
# All ORM models will inherit from this base class.
# It maintains a registry of all model metadata.
# ------------------------------------------------------------
Base = declarative_base()


# ------------------------------------------------------------
# Function: get_db
# Description:
#   Provides a database session for dependency injection (e.g., in FastAPI routes).
#   Ensures that sessions are properly closed after use.
#
# Usage Example:
#   db = get_db()
#   result = db.query(User).all()
# ------------------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()
        engine.dispose()
