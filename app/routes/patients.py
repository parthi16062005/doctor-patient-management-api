from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.patient import Patient
from app.models.doctor import Doctor
from app.models.user import User

from app.schemas.patient import (
    PatientCreate,
    PatientUpdate,
    PatientResponse,
    PatientListResponse
)

from app.dependencies import admin_required

from app.services.patient_service import (
    create_patient,
    get_patient_by_id,
    get_patients,
    update_patient,
    patch_patient,
    delete_patient
)


router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)


# ==================================================
# CREATE PATIENT
# ==================================================

@router.post(
    "/",
    response_model=PatientResponse,
    status_code=201
)
def create_patient_api(
    patient: PatientCreate,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        admin_required
    )
):

    # Check doctor if doctor_id is provided
    if patient.doctor_id is not None:

        doctor = db.query(Doctor).filter(
            Doctor.id == patient.doctor_id
        ).first()

        if not doctor:
            raise HTTPException(
                status_code=404,
                detail="Doctor not found"
            )

        if not doctor.is_active:
            raise HTTPException(
                status_code=400,
                detail="Cannot assign patient to an inactive doctor"
            )

    return create_patient(
        db=db,
        name=patient.name,
        age=patient.age,
        phone=patient.phone,
        doctor_id=patient.doctor_id
    )


# ==================================================
# GET ALL PATIENTS
# Filtering + Pagination
# ==================================================

@router.get(
    "/",
    response_model=PatientListResponse
)
def get_patients_api(
    age_gt: int | None = Query(
        default=None,
        gt=0
    ),

    page: int = Query(
        default=1,
        ge=1
    ),

    limit: int = Query(
        default=10,
        ge=1,
        le=100
    ),

    db: Session = Depends(get_db),

    current_user: User = Depends(
        admin_required
    )
):

    total, patients = get_patients(
        db=db,
        age_gt=age_gt,
        page=page,
        limit=limit
    )

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "data": patients
    }


# ==================================================
# GET ONE PATIENT
# ==================================================

@router.get(
    "/{patient_id}",
    response_model=PatientResponse
)
def get_patient_api(
    patient_id: int,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        admin_required
    )
):

    patient = get_patient_by_id(
        db=db,
        patient_id=patient_id
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return patient


# ==================================================
# UPDATE PATIENT
# PUT
# ==================================================

@router.put(
    "/{patient_id}",
    response_model=PatientResponse
)
def update_patient_api(
    patient_id: int,

    patient_data: PatientCreate,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        admin_required
    )
):

    patient = get_patient_by_id(
        db=db,
        patient_id=patient_id
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    # Check doctor
    if patient_data.doctor_id is not None:

        doctor = db.query(Doctor).filter(
            Doctor.id == patient_data.doctor_id
        ).first()

        if not doctor:
            raise HTTPException(
                status_code=404,
                detail="Doctor not found"
            )

        if not doctor.is_active:
            raise HTTPException(
                status_code=400,
                detail="Cannot assign patient to an inactive doctor"
            )

    return update_patient(
        db=db,
        patient=patient,
        name=patient_data.name,
        age=patient_data.age,
        phone=patient_data.phone,
        doctor_id=patient_data.doctor_id
    )


# ==================================================
# PARTIAL UPDATE PATIENT
# PATCH
# ==================================================

@router.patch(
    "/{patient_id}",
    response_model=PatientResponse
)
def patch_patient_api(
    patient_id: int,

    patient_data: PatientUpdate,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        admin_required
    )
):

    patient = get_patient_by_id(
        db=db,
        patient_id=patient_id
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    update_data = patient_data.model_dump(
        exclude_unset=True
    )

    # Check doctor if doctor_id is provided
    if "doctor_id" in update_data:

        doctor_id = update_data["doctor_id"]

        if doctor_id is not None:

            doctor = db.query(Doctor).filter(
                Doctor.id == doctor_id
            ).first()

            if not doctor:
                raise HTTPException(
                    status_code=404,
                    detail="Doctor not found"
                )

            if not doctor.is_active:
                raise HTTPException(
                    status_code=400,
                    detail="Cannot assign patient to an inactive doctor"
                )

    return patch_patient(
        db=db,
        patient=patient,
        update_data=update_data
    )


# ==================================================
# DELETE PATIENT
# ==================================================

@router.delete(
    "/{patient_id}",
    status_code=204
)
def delete_patient_api(
    patient_id: int,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        admin_required
    )
):

    patient = get_patient_by_id(
        db=db,
        patient_id=patient_id
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    delete_patient(
        db=db,
        patient=patient
    )

    return None