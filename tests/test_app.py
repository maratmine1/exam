from fastapi.testclient import TestClient

from app.main import app, init_db


client = TestClient(app)


def setup_module(module):
    init_db()


def test_get_cars():
    response = client.get("/cars")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["is_reserved"] is False


def test_get_car_info_success():
    payload = {"phone": "+79846274627", "sms_code": "1420"}
    response = client.post("/car-info", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "car_model" in data
    assert "car_number" in data
    assert "fuel_level" in data


def test_get_car_info_invalid_auth():
    payload = {"phone": "+70000000000", "sms_code": "0000"}
    response = client.post("/car-info", json=payload)
    assert response.status_code == 401

