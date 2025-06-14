from fastapi.testclient import TestClient
from app.api.main import app

client = TestClient(app)


def test_no_face():
    response = client.post("/analyze_face_traits", files={"file": ("test.jpg", b"dummy", "image/jpeg")})
    assert response.status_code == 400


def test_disclaimer_present():
    with open("ann.jpg", "rb") as f:
        img_bytes = f.read()
    response = client.post("/analyze_face_traits", files={"file": ("img.jpg", img_bytes, "image/jpeg")})
    assert "disclaimer" in response.json()
    assert response.status_code == 200
