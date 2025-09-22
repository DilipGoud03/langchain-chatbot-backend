from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from decouple import config
import os
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = "{}://{}:{}@{}:{}/{}".format(
    config("DB_ENGINE"),
    config("MYSQL_USER"),
    config("MYSQL_PASSWORD"),
    config("MYSQL_URL"),
    config("MYSQL_PORT"),
    config("MYSQL_DB"),
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=5,
    pool_pre_ping=True,
    isolation_level="READ COMMITTED",
)

SessionLocal = sessionmaker(bind=engine)
SessionLocal = scoped_session(SessionLocal)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()
        engine.dispose()
