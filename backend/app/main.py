from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.auth import router as auth_router
from app.api.v1.documents import router as documents_router
from app.api.v1.review import router as review_router
from app.api.v1.patients import router as patients_router


app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
print("Starting FastAPI application...")
app.include_router(auth_router)
app.include_router(documents_router)
app.include_router(review_router)
app.include_router(patients_router)
