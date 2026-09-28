
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine

from app.api.auth import router as auth_router
from app.api.doctor_patient_router import router as doctor_patient_router

from app.routes.doctors import router as doctor_router
from app.routes.patients import router as patient_router

from app.logging_config import setup_logging


# ==================================================
# LOGGING
# ==================================================

setup_logging()


# ==================================================
# CREATE DATABASE TABLES
# ==================================================

Base.metadata.create_all(
    bind=engine
)


# ==================================================
# FASTAPI APPLICATION
# ==================================================

app = FastAPI(
    title="Doctor Patient Management API",
    description="Backend API for managing Doctors and Patients",
    version="1.0.0"
)


# ==================================================
# CORS
# ==================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# ==================================================
# API V1 ROUTES
# ==================================================

app.include_router(
    auth_router,
    prefix="/api/v1"
)

app.include_router(
    doctor_router,
    prefix="/api/v1"
)

app.include_router(
    patient_router,
    prefix="/api/v1"
)

app.include_router(
    doctor_patient_router,
    prefix="/api/v1"
)


# ==================================================
# HOME
# ==================================================

@app.get("/")
def home():

    return {
        "message": "Doctor Patient Management API is working!"
    }

