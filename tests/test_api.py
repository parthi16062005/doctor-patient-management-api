
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_home():

    response = client.get("/")

    assert response.status_code == 200

    assert response.json() == {
        "message": "Doctor Patient Management API is working!"
    }


def test_invalid_doctor():

    response = client.get(
        "/doctors/99999"
    )

    assert response.status_code in [401, 403, 404]

