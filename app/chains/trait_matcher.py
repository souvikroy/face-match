from __future__ import annotations
from typing import Dict, List


class TraitMatcher:
    def match(self, tags_text: str, candidate_traits: List[Dict]) -> List[Dict]:
        results = []
        for trait in candidate_traits:
            plausible = hash(tags_text + trait["trait"]) % 2 == 0
            results.append({
                "trait": trait["trait"],
                "plausible": plausible,
                "reason": "stub",
                "similarity": trait.get("similarity", 0),
            })
        return results
