from __future__ import annotations

import json
from pathlib import Path
from typing import List, Dict, Tuple

import numpy as np
from openai import OpenAIError
from langchain.embeddings import OpenAIEmbeddings

from .config import settings


def load_traits(path: Path) -> List[Dict]:
    data = json.loads(path.read_text())
    return data


class TraitEmbedder:
    def __init__(self, traits_path: Path):
        self.traits_path = traits_path
        self.traits = load_traits(traits_path)
        self.embeddings_model = OpenAIEmbeddings(openai_api_key=settings.openai_api_key,
                                                 model=settings.embedding_model)
        self.trait_texts = [f"{t['trait']}: {t.get('description', '')}" for t in self.traits]
        self.trait_embeddings = self._embed_texts(self.trait_texts)

    def _embed_texts(self, texts: List[str]) -> np.ndarray:
        try:
            embeds = self.embeddings_model.embed_documents(texts)
        except OpenAIError as e:
            raise RuntimeError(f"Embedding error: {e}")
        return np.array(embeds)

    def embed_tags(self, tags_text: str) -> np.ndarray:
        return np.array(self.embeddings_model.embed_query(tags_text))

    def find_similar_traits(self, tags_embedding: np.ndarray, top_n: int) -> List[Tuple[Dict, float]]:
        sims = self.trait_embeddings @ tags_embedding / (
            np.linalg.norm(self.trait_embeddings, axis=1) * np.linalg.norm(tags_embedding) + 1e-8)
        idx = np.argsort(sims)[::-1][:top_n]
        return [(self.traits[i], float(sims[i])) for i in idx]
