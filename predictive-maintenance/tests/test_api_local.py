import requests

BASE_URL = "http://localhost:8000"


def test_health():
    r = requests.get(f"{BASE_URL}/health")
    assert r.status_code == 200
    data = r.json()
    assert data["model_loaded"] is True


def test_predict():
    payload = {
        "data": [
            {
                "temperature": 50 + i * 0.5,
                "pressure": 100 + i * 0.5,
                "vibration": 5 + i * 0.1,
                "rpm": 3000 + i * 10,
                "torque": 50 + i * 0.2,
                "fuel_flow": 200 + i,
            }
            for i in range(24)
        ]
    }
    r = requests.post(f"{BASE_URL}/predict", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "prediction" in data
    assert "probability" in data
