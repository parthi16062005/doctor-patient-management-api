# Doctor Patient Management API

A backend REST API built using **FastAPI** for managing doctors and patients.

The project includes authentication, authorization, database persistence, doctor-patient relationships, CRUD operations, validation, filtering, pagination, logging, API versioning, and automated testing.

## Features

* JWT Authentication
* Role-based Authorization
* Doctor Management
* Patient Management
* Doctor-Patient Relationship
* Doctor Soft Delete
* Complete CRUD Operations
* Partial Update using PATCH
* Email Validation
* Unique Doctor Email
* 10-Digit Patient Phone Validation
* Filtering
* Pagination
* SQLite Database
* SQLAlchemy ORM
* Alembic Database Migration
* CORS
* Environment Variables using `.env`
* Application Logging
* API Versioning using `/api/v1`
* Automated Testing using Pytest
* Dockerfile included

## Technology Stack

* Python 3.14
* FastAPI
* Pydantic
* SQLAlchemy
* SQLite
* JWT
* python-jose
* Passlib
* bcrypt
* Alembic
* Pytest
* Uvicorn
* Docker

## Project Structure

```text
doctor_patient_api/
│
├── app/
│   ├── api/
│   │   ├── auth.py
│   │   └── doctor_patient_router.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── doctor.py
│   │   └── patient.py
│   │
│   ├── schemas/
│   │   ├── user.py
│   │   ├── doctor.py
│   │   └── patient.py
│   │
│   ├── routes/
│   │   ├── doctors.py
│   │   └── patients.py
│   │
│   ├── services/
│   │   ├── doctor_service.py
│   │   └── patient_service.py
│   │
│   ├── auth.py
│   ├── database.py
│   ├── dependencies.py
│   ├── logging_config.py
│   └── main.py
│
├── alembic/
├── tests/
│   └── test_api.py
│
├── Dockerfile
├── pytest.ini
├── alembic.ini
├── create_admin.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## API Version

All main APIs use:

```text
/api/v1
```

### Authentication

```text
POST /api/v1/auth/register
POST /api/v1/auth/login
```

### Doctors

```text
POST   /api/v1/doctors/
GET    /api/v1/doctors/
GET    /api/v1/doctors/{doctor_id}
PUT    /api/v1/doctors/{doctor_id}
PATCH  /api/v1/doctors/{doctor_id}
DELETE /api/v1/doctors/{doctor_id}
```

### Patients

```text
POST   /api/v1/patients/
GET    /api/v1/patients/
GET    /api/v1/patients/{patient_id}
PUT    /api/v1/patients/{patient_id}
PATCH  /api/v1/patients/{patient_id}
DELETE /api/v1/patients/{patient_id}
```

### Doctor-Patient

```text
POST /api/v1/doctor-patient/{doctor_id}/patients/{patient_id}

GET /api/v1/doctor-patient/{doctor_id}/patients
```

## Filtering

Doctors can be filtered by specialization:

```text
GET /api/v1/doctors/?specialization=Cardiology
```

Doctors can also be filtered by active status:

```text
GET /api/v1/doctors/?is_active=true
```

Patients can be filtered by age:

```text
GET /api/v1/patients/?age_gt=30
```

## Pagination

Doctors:

```text
GET /api/v1/doctors/?page=1&limit=10
```

Patients:

```text
GET /api/v1/patients/?page=1&limit=10
```

The response contains:

```json
{
    "total": 0,
    "page": 1,
    "limit": 10,
    "data": []
}
```

## Validation

### Doctor Email

Doctor email must be a valid email address and must be unique.

### Patient Phone

Patient phone number must contain exactly 10 numeric digits.

Example:

```text
9876543210
```

### Patient Age

Patient age must be greater than 0.

## Authentication

The application uses **JWT Bearer Authentication**.

After successful login, the API returns an access token.

The token can be used in Swagger using the **Authorize** button.

Protected operations require authentication.

Administrative operations such as creating, updating, and deleting doctors and patients require appropriate authorization.

## Database

The project uses:

* SQLite
* SQLAlchemy ORM

Database file:

```text
doctor_patient.db
```

## Alembic

Alembic is used for database migration management.

Example commands:

```powershell
alembic revision --autogenerate -m "migration message"
```

```powershell
alembic upgrade head
```

## Logging

Application logging is enabled using Python's logging module.

Example:

```text
INFO - Logging system started
```

## CORS

CORS middleware is configured in the FastAPI application to support cross-origin requests.

## Environment Variables

Sensitive configuration is stored in `.env`.

Example:

```text
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

The `.env` file is excluded from Git using `.gitignore`.

## Running the Project

### 1. Create Virtual Environment

```powershell
python -m venv venv
```

### 2. Activate Virtual Environment

```powershell
venv\Scripts\activate
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Then:

```powershell
venv\Scripts\activate
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Run the Application

```powershell
uvicorn app.main:app --reload
```

### 5. Open Swagger

```text
http://127.0.0.1:8000/docs
```

## Running Tests

Run:

```powershell
pytest
```

Current tests:

```text
2 passed
```

## Docker

A Dockerfile is included in the project for container deployment.

Docker was not tested locally during development because Docker Desktop was not installed.

## Project Status

The project implements the requested backend enhancement levels including:

* Relationship & Business Logic
* CRUD & Soft Delete
* Advanced Validation
* Filtering
* Pagination
* Clean Project Structure
* Database Integration
* Alembic Migration
* JWT Authentication
* Logging
* CORS
* Environment Configuration
* Dockerfile
* Pytest
* API Versioning
