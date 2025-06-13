from __future__ import annotations

from typing import Dict, List

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
import json

from ..config import settings


class TraitMatcher:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0.7, model=settings.llm_model,
                              openai_api_key=settings.openai_api_key)

    def match(self, tags_text: str, candidate_traits: List[Dict]) -> List[Dict]:
        results = []
        for trait in candidate_traits:
            prompt = (
                "You are an AI assistant.\n"
                f"Facial tags: {tags_text}\n"
                f"Candidate trait: {trait['trait']} - {trait.get('description', '')}\n"
                "Evaluate plausibility cautiously. Respond in JSON with fields 'trait', 'plausible', and 'reason'."
            )
            msg = self.llm([HumanMessage(content=prompt)])
            try:
                parsed = json.loads(msg.content)
            except json.JSONDecodeError:
                parsed = {
                    "trait": trait["trait"],
                    "plausible": False,
                    "reason": "LLM response could not be parsed"
                }
            parsed["similarity"] = trait.get("similarity", 0)
            results.append(parsed)
        return results
