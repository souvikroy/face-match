from __future__ import annotations

import json
import hashlib
from pathlib import Path
from typing import List, Dict, Tuple


def load_traits(path: Path) -> List[Dict]:
    return json.loads(path.read_text())


def _text_to_vec(text: str) -> List[int]:
    h = hashlib.sha256(text.encode()).digest()
    return [b for b in h[:8]]


def _cosine(v1: List[int], v2: List[int]) -> float:
    dot = sum(a * b for a, b in zip(v1, v2))
    norm1 = sum(a * a for a in v1) ** 0.5
    norm2 = sum(b * b for b in v2) ** 0.5
    return dot / (norm1 * norm2 + 1e-8)


class TraitEmbedder:
    def __init__(self, traits_path: Path):
        self.traits = load_traits(traits_path)
        self.trait_texts = [f"{t['trait']}: {t.get('description', '')}" for t in self.traits]
        self.trait_embeddings = [_text_to_vec(t) for t in self.trait_texts]

    def embed_tags(self, tags_text: str) -> List[int]:
        return _text_to_vec(tags_text)

    def find_similar_traits(self, tags_embedding: List[int], top_n: int) -> List[Tuple[Dict, float]]:
        sims = [_cosine(tags_embedding, e) for e in self.trait_embeddings]
        idx_sims = sorted(enumerate(sims), key=lambda x: x[1], reverse=True)[:top_n]
        return [(self.traits[i], float(sim)) for i, sim in idx_sims]
