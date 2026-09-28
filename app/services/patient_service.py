from sqlalchemy.orm import Session

from app.models.patient import Patient


# ==================================================
# CREATE PATIENT
# ==================================================

def create_patient(
    db: Session,
    name: str,
    age: int,
    phone: str,
    doctor_id: int | None
):

    patient = Patient(
        name=name,
        age=age,
        phone=phone,
        doctor_id=doctor_id
    )

    db.add(patient)
    db.commit()
    db.refresh(patient)

    return patient


# ==================================================
# GET PATIENT BY ID
# ==================================================

def get_patient_by_id(
    db: Session,
    patient_id: int
):

    return db.query(Patient).filter(
        Patient.id == patient_id
    ).first()


# ==================================================
# GET PATIENTS
# Filtering + Pagination
# ==================================================

def get_patients(
    db: Session,
    age_gt=None,
    page=1,
    limit=10
):

    query = db.query(Patient)

    if age_gt is not None:

        query = query.filter(
            Patient.age > age_gt
        )

    total = query.count()

    offset = (page - 1) * limit

    patients = query.offset(
        offset
    ).limit(
        limit
    ).all()

    return total, patients


# ==================================================
# UPDATE PATIENT
# ==================================================

def update_patient(
    db: Session,
    patient,
    name,
    age,
    phone,
    doctor_id
):

    patient.name = name
    patient.age = age
    patient.phone = phone
    patient.doctor_id = doctor_id

    db.commit()
    db.refresh(patient)

    return patient


# ==================================================
# PATCH PATIENT
# ==================================================

def patch_patient(
    db: Session,
    patient,
    update_data
):

    for field, value in update_data.items():

        setattr(
            patient,
            field,
            value
        )

    db.commit()
    db.refresh(patient)

    return patient


# ==================================================
# DELETE PATIENT
# ==================================================

def delete_patient(
    db: Session,
    patient
):

    db.delete(patient)

    db.commit()