from sqlalchemy.orm import Session

from app.models.doctor import Doctor


# ==================================================
# CREATE DOCTOR
# ==================================================

def create_doctor(
    db: Session,
    name: str,
    specialization: str,
    email: str
):

    doctor = Doctor(
        name=name,
        specialization=specialization,
        email=email,
        is_active=True
    )

    db.add(doctor)
    db.commit()
    db.refresh(doctor)

    return doctor


# ==================================================
# GET DOCTOR BY ID
# ==================================================

def get_doctor_by_id(
    db: Session,
    doctor_id: int
):

    return db.query(Doctor).filter(
        Doctor.id == doctor_id
    ).first()


# ==================================================
# GET DOCTORS
# ==================================================

def get_doctors(
    db: Session,
    specialization=None,
    is_active=None,
    page=1,
    limit=10
):

    query = db.query(Doctor)

    if specialization is not None:

        query = query.filter(
            Doctor.specialization.ilike(
                specialization
            )
        )

    if is_active is not None:

        query = query.filter(
            Doctor.is_active == is_active
        )

    total = query.count()

    offset = (page - 1) * limit

    doctors = query.offset(
        offset
    ).limit(
        limit
    ).all()

    return total, doctors


# ==================================================
# UPDATE DOCTOR
# ==================================================

def update_doctor(
    db: Session,
    doctor,
    name,
    specialization,
    email
):

    doctor.name = name
    doctor.specialization = specialization
    doctor.email = email

    db.commit()
    db.refresh(doctor)

    return doctor


# ==================================================
# PATCH DOCTOR
# ==================================================

def patch_doctor(
    db: Session,
    doctor,
    update_data
):

    for field, value in update_data.items():

        setattr(
            doctor,
            field,
            value
        )

    db.commit()
    db.refresh(doctor)

    return doctor


# ==================================================
# SOFT DELETE DOCTOR
# ==================================================

def delete_doctor(
    db: Session,
    doctor
):

    doctor.is_active = False

    db.commit()
    db.refresh(doctor)

    return doctor