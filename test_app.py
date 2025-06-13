import json
from pathlib import Path

from fastapi.testclient import TestClient

from app.api.main import app

client = TestClient(app)


def test_no_face():
    response = client.post("/analyze_face_traits", files={"file": ("test.jpg", b"dummy", "image/jpeg")})
    assert response.status_code == 400


def test_disclaimer_present():
    # Use a very small black image with no face
    import numpy as np
    import cv2
    img = np.zeros((10, 10, 3), dtype=np.uint8)
    _, buf = cv2.imencode('.jpg', img)
    response = client.post("/analyze_face_traits", files={"file": ("img.jpg", buf.tobytes(), "image/jpeg")})
    assert "disclaimer" in response.json()
