# test_db.py

from sqlalchemy import create_engine

DATABASE_URL = "postgresql://admin:admin123@localhost:5432/healthcare"

engine = create_engine(DATABASE_URL)

try:
    with engine.connect():
        print("✅ Connected")
except Exception as e:
    print(e)