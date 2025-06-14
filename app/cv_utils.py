from __future__ import annotations
from typing import Dict, List, Tuple

# Stub implementations without external dependencies

def detect_faces(image_bytes: bytes) -> Tuple[bytes, List[Tuple[int, int, int, int]]]:
    """Very naive face detection stub."""
    # If the bytes look like a JPEG (start with 0xFFD8), pretend we found one face
    if image_bytes.startswith(b"\xff\xd8"):
        return image_bytes, [(0, 1, 1, 0)]
    return image_bytes, []


def extract_basic_tags(image: bytes, box: Tuple[int, int, int, int]) -> Dict:
    mean_intensity = sum(image) / (len(image) or 1) / 255.0
    tags = {"mean_intensity": mean_intensity}
    tags_text = f"mean_intensity:{mean_intensity:.2f}"
    return tags, tags_text
