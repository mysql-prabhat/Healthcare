from datetime import date

from pydantic import BaseModel
from typing import Optional
from typing import Literal

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    tenant_id: str
    
class ReviewRequest(BaseModel):
    approved: bool
    comments: Optional[str] = None

class PatientCreate(BaseModel):
    patient_id: str
    first_name: str
    last_name: str
    dob: date
    gender: Literal[
        "Male",
        "Female",
        "Other"
    ]

class PatientResponse(BaseModel):
    id: int
    patient_id: str
    first_name: str
    last_name: str
    dob: date
    gender: str

    class Config:
        from_attributes = True