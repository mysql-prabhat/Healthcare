from fastapi import Depends, HTTPException
from app.core.auth import get_current_user

def require_reviewer():

    def checker(
        user=Depends(get_current_user)
    ):

        if user["role"] not in [
            "reviewer",
            "admin"
        ]:
            raise HTTPException(
                status_code=403,
                detail="Access denied"
            )

        return user

    return checker

def require_admin():

    def checker(
        user=Depends(get_current_user)
    ):
        if user["role"] != "admin":
            raise HTTPException(
                status_code=403,
                detail="Admin access required"
            )

        return user

    return checker

def require_roles(roles: list):

    def checker(
        user=Depends(get_current_user)
    ):
        if user["role"] not in roles:
            raise HTTPException(
                status_code=403,
                detail="Access denied"
            )

        return user

    return checker