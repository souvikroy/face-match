from __future__ import annotations

import tempfile
from typing import Dict, List, Tuple

try:
    import cv2
except Exception:  # pragma: no cover - optional dependency may not be installed
    cv2 = None
try:
    import face_recognition
except Exception:  # pragma: no cover - optional dependency may not be installed
    face_recognition = None
import numpy as np


# Simple facial tag extraction using face_recognition and cv2. This is a
# lightweight placeholder; real models would provide richer outputs.
def detect_faces(image_bytes: bytes) -> Tuple[np.ndarray, List[Tuple[int, int, int, int]]]:
    """Detect faces using whatever backend is available."""
    with tempfile.NamedTemporaryFile(suffix=".jpg") as tmp:
        tmp.write(image_bytes)
        tmp.flush()
        if face_recognition:
            image = face_recognition.load_image_file(tmp.name)
            boxes = face_recognition.face_locations(image)
        elif cv2:
            image = cv2.imread(tmp.name)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
            rects = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
            boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]
        else:
            raise RuntimeError("No face detection backend available")
    return image, boxes


def extract_basic_tags(image: np.ndarray, box: Tuple[int, int, int, int]) -> Dict:
    top, right, bottom, left = box
    face_img = image[top:bottom, left:right]
    if cv2 is None:
        raise RuntimeError("cv2 is required for tag extraction")
    gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
    mean_intensity = float(np.mean(gray)) / 255.0
    tags = {
        "mean_intensity": mean_intensity,
    }
    tags_text = f"mean_intensity:{mean_intensity:.2f}"
    return tags, tags_text
