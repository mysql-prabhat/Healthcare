# create_tables.py

import os
import sys
from sqlalchemy import text

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

from app.core.db import engine
from app.core.models import *

Base.metadata.create_all(bind=engine)

with engine.begin() as connection:
    for column, column_type in (
        ("tenant_id", "VARCHAR"),
        ("title", "VARCHAR"),
        ("file_name", "VARCHAR"),
        ("file_path", "VARCHAR"),
        ("file_type", "VARCHAR"),
        ("extracted_text", "TEXT"),
        ("summary", "TEXT"),
        ("recommendations", "TEXT"),
        ("confidence_score", "FLOAT"),
        ("status", "VARCHAR"),
        ("created_at", "TIMESTAMP"),
    ):
        connection.execute(
            text(
                f"ALTER TABLE documents "
                f"ADD COLUMN IF NOT EXISTS {column} {column_type}"
            )
        )

print("Tables Created")