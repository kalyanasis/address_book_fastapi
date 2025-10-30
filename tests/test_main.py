from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_and_get_address():
    response = client.post("/addresses/", json={
        "name": "Home",
        "street": "123 Street",
        "city": "Cityville",
        "latitude": 12.9716,
        "longitude": 77.5946
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Home"
    address_id = data["id"]

    get_response = client.get(f"/addresses/{address_id}")
    assert get_response.status_code == 200
    assert get_response.json()["city"] == "Cityville"
