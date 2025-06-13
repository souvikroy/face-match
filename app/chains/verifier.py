from __future__ import annotations

from typing import List, Dict

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
import json

from ..config import settings


class Verifier:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0.3, model=settings.llm_model,
                              openai_api_key=settings.openai_api_key)

    def verify(self, tags_text: str, initial_results: List[Dict]) -> List[Dict]:
        verified = []
        for res in initial_results:
            prompt = (
                "You are an expert psychologist.\n"
                f"Facial tags: {tags_text}\n"
                f"Initial inference: {res}\n"
                "Critically assess any bias or overreach. Reply in JSON with fields 'trait', 'verified', 'reason'."
            )
            msg = self.llm([HumanMessage(content=prompt)])
            try:
                parsed = json.loads(msg.content)
            except json.JSONDecodeError:
                parsed = {
                    "trait": res.get("trait"),
                    "verified": False,
                    "reason": "LLM response could not be parsed"
                }
            verified.append(parsed)
        return verified
