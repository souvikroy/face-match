from __future__ import annotations

from typing import List, Dict

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

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
                f"Initial inference: {res['llm_response']}\n"
                "Critically assess any bias or overreach. Reply in JSON with fields 'trait', 'verified', 'reason'."
            )
            msg = self.llm([HumanMessage(content=prompt)])
            verified.append({
                "trait": res["trait"],
                "verifier_response": msg.content,
            })
        return verified
