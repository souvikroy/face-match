from __future__ import annotations
from typing import List, Dict


class Verifier:
    def verify(self, tags_text: str, initial_results: List[Dict]) -> List[Dict]:
        verified = []
        for res in initial_results:
            verified.append({
                "trait": res.get("trait"),
                "verified": res.get("plausible", False),
                "reason": "stub",
            })
        return verified
