from __future__ import annotations

import logging
from pathlib import Path
from typing import List

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from ..config import settings
from ..cv_utils import detect_faces, extract_basic_tags
from ..embedding_utils import TraitEmbedder
from ..chains.trait_matcher import TraitMatcher
from ..chains.verifier import Verifier

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Face Trait Matcher")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] ,
    allow_methods=["*"] ,
    allow_headers=["*"] ,
)

traits_path = Path(__file__).resolve().parents[2] / "traits.json"
trait_embedder = TraitEmbedder(traits_path)
trait_matcher = TraitMatcher()
verifier = Verifier()

DISCLAIMER = (
    "This system is experimental. Inferring psychological traits from facial appearance is highly speculative,"
    " potentially biased, and should not be used for important decisions."
)


@app.post("/analyze_face_traits")
async def analyze_face_traits(file: UploadFile = File(...)):
    content = await file.read()
    image, boxes = detect_faces(content)
    if not boxes:
        raise HTTPException(status_code=400, detail="No face detected")
    faces = []
    for i, box in enumerate(boxes):
        tags, tags_text = extract_basic_tags(image, box)
        tags_embedding = trait_embedder.embed_tags(tags_text)
        sim_traits = trait_embedder.find_similar_traits(tags_embedding, settings.top_n)
        for trait, score in sim_traits:
            trait["similarity"] = score
        initial = trait_matcher.match(tags_text, [t for t, _ in sim_traits])
        verified = verifier.verify(tags_text, initial) if settings.use_verifier else []
        faces.append({
            "face_id": i + 1,
            "bounding_box": {
                "top": box[0],
                "right": box[1],
                "bottom": box[2],
                "left": box[3],
            },
            "tags": tags,
            "initial_matches": initial,
            "verifier_results": verified,
        })
    return {"faces": faces, "disclaimer": DISCLAIMER}
