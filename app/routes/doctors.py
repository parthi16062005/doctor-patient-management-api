from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.doctor import Doctor
from app.models.user import User

from app.schemas.doctor import (
    DoctorCreate,
    DoctorUpdate,
    DoctorResponse,
    DoctorListResponse
)

from app.dependencies import (
    get_current_user,
    admin_required
)

from app.services.doctor_service import (
    create_doctor,
    get_doctor_by_id,
    get_doctors,
    update_doctor,
    patch_doctor,
    delete_doctor
)


router = APIRouter(
    prefix="/doctors",
    tags=["Doctors"]
)


# ==================================================
# CREATE DOCTOR
# ==================================================

@router.post(
    "/",
    response_model=DoctorResponse,
    status_code=201
)
def create_doctor_api(
    doctor: DoctorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):

    existing_doctor = db.query(Doctor).filter(
        Doctor.email == doctor.email
    ).first()

    if existing_doctor:
        raise HTTPException(
            status_code=400,
            detail="Doctor email already exists"
        )

    return create_doctor(
        db=db,
        name=doctor.name,
        specialization=doctor.specialization,
        email=doctor.email
    )


# ==================================================
# GET ALL DOCTORS
# Filtering + Pagination
# ==================================================

@router.get(
    "/",
    response_model=DoctorListResponse
)
def get_doctors_api(
    specialization: str | None = Query(
        default=None
    ),

    is_active: bool | None = Query(
        default=None
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
        get_current_user
    )
):

    total, doctors = get_doctors(
        db=db,
        specialization=specialization,
        is_active=is_active,
        page=page,
        limit=limit
    )

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "data": doctors
    }


# ==================================================
# GET ONE DOCTOR
# ==================================================

@router.get(
    "/{doctor_id}",
    response_model=DoctorResponse
)
def get_doctor_api(
    doctor_id: int,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    doctor = get_doctor_by_id(
        db=db,
        doctor_id=doctor_id
    )

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    return doctor


# ==================================================
# UPDATE DOCTOR
# PUT
# ==================================================

@router.put(
    "/{doctor_id}",
    response_model=DoctorResponse
)
def update_doctor_api(
    doctor_id: int,

    doctor_data: DoctorCreate,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        admin_required
    )
):

    doctor = get_doctor_by_id(
        db=db,
        doctor_id=doctor_id
    )

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    existing_doctor = db.query(Doctor).filter(
        Doctor.email == doctor_data.email,
        Doctor.id != doctor_id
    ).first()

    if existing_doctor:
        raise HTTPException(
            status_code=400,
            detail="Doctor email already exists"
        )

    return update_doctor(
        db=db,
        doctor=doctor,
        name=doctor_data.name,
        specialization=doctor_data.specialization,
        email=doctor_data.email
    )


# ==================================================
# PARTIAL UPDATE DOCTOR
# PATCH
# ==================================================

@router.patch(
    "/{doctor_id}",
    response_model=DoctorResponse
)
def patch_doctor_api(
    doctor_id: int,

    doctor_data: DoctorUpdate,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        admin_required
    )
):

    doctor = get_doctor_by_id(
        db=db,
        doctor_id=doctor_id
    )

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    update_data = doctor_data.model_dump(
        exclude_unset=True
    )

    if "email" in update_data:

        existing_doctor = db.query(Doctor).filter(
            Doctor.email == update_data["email"],
            Doctor.id != doctor_id
        ).first()

        if existing_doctor:
            raise HTTPException(
                status_code=400,
                detail="Doctor email already exists"
            )

    return patch_doctor(
        db=db,
        doctor=doctor,
        update_data=update_data
    )


# ==================================================
# SOFT DELETE DOCTOR
# ==================================================

@router.delete(
    "/{doctor_id}",
    response_model=DoctorResponse
)
def delete_doctor_api(
    doctor_id: int,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        admin_required
    )
):

    doctor = get_doctor_by_id(
        db=db,
        doctor_id=doctor_id
    )

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    return delete_doctor(
        db=db,
        doctor=doctor
    )