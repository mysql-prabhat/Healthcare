import os

from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://admin:admin123@localhost:5432/healthcare" or os.environ.get("DATABASE_URL")
DATABASE_URL = os.environ.get("DATABASE_URL") or DATABASE_URL

database_host = os.environ.get("DATABASE_HOST")
if database_host:
    DATABASE_URL = make_url(DATABASE_URL).set(host=database_host)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()