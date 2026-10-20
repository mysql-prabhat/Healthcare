
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.schemas import LoginRequest
from app.core.db import get_db
from app.core.models import User
from app.core.auth import (
    create_access_token,
    get_current_user,
    verify_password,
)

router = APIRouter(
    prefix="/v1/auth",
    tags=["Authentication"]
)
print("Authentication router initialized...")
@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = (
        db.query(User)
        .filter(User.username == request.username)
        .first()
    )
    if not user or not user.password_hash or not verify_password(
        request.password, user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username/password"
        )

    token = create_access_token({
        "sub": user.username,
        "role": user.role,
        "tenant_id": user.tenant_id
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.get("/me")
def me(
    user=Depends(get_current_user)
):
    return user