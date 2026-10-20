# seed.py

import os
import sys

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

from passlib.context import CryptContext


from app.core.db import SessionLocal
from app.core.models import User

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

db = SessionLocal()

password = pwd_context.hash(
    "admin123"
)

print(password)
admin = User(
    username="admin",
    password_hash=pwd_context.hash("admin123"),
    role="admin",
    tenant_id="tenant-001"
)

reviewer = User(
    username="doctor",
    password_hash=pwd_context.hash("doctor123"),
    role="reviewer",
    tenant_id="tenant-001"
)

db.add(admin)
db.add(reviewer)

db.commit()

print("Seed completed")