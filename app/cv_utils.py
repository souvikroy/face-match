from __future__ import annotations

import tempfile
from typing import Dict, List, Tuple

import cv2
import face_recognition
import numpy as np


# Simple facial tag extraction using face_recognition and cv2. This is a
# lightweight placeholder; real models would provide richer outputs.
def detect_faces(image_bytes: bytes) -> Tuple[np.ndarray, List[Tuple[int, int, int, int]]]:
    with tempfile.NamedTemporaryFile(suffix=".jpg") as tmp:
        tmp.write(image_bytes)
        tmp.flush()
        image = face_recognition.load_image_file(tmp.name)
    boxes = face_recognition.face_locations(image)
    return image, boxes


def extract_basic_tags(image: np.ndarray, box: Tuple[int, int, int, int]) -> Dict:
    top, right, bottom, left = box
    face_img = image[top:bottom, left:right]
    gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
    mean_intensity = float(np.mean(gray)) / 255.0
    tags = {
        "mean_intensity": mean_intensity,
    }
    tags_text = f"mean_intensity:{mean_intensity:.2f}"
    return tags, tags_text
