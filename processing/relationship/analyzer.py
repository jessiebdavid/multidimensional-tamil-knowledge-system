from typing import Any, Dict, List


RELATIONSHIP_TYPES = {
    "FACT",
    "INTERPRETATION",
    "ANALOGY",
    "HYPOTHESIS",
    "UNSUPPORTED",
}


class RelationshipAnalyzer:
    """
    Classifies relationships between scientific concepts and
    retrieved Tamil-literature evidence.

    Retrieval relevance and relationship confidence are kept separate.
    """

    def analyze(
        self,
        scientific_concepts: List[str],
        retrieved_results: List[Dict[str, Any]],
    ) -> Dict[str, Any]:

        if not retrieved_results:
            return self._unsupported(
                scientific_concepts,
                "No retrieved literary evidence was available.",
            )

        evidence = self._build_evidence(retrieved_results)

        relationship_type = self._classify(evidence)

        confidence = self._confidence(
            relationship_type,
            evidence,
        )

        return {
            "relationship_type": relationship_type,
            "relationship_confidence": confidence,
            "scientific_concepts": scientific_concepts,
            "evidence": evidence,
            "reason": self._reason(relationship_type),
        }

    def _build_evidence(
        self,
        retrieved_results: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:

        return [
            {
                "source_id": result.get("source_id", ""),
                "source_type": result.get("source_type", ""),
                "text": result.get("text", ""),
                "retrieval_score": result.get(
                    "retrieval_score",
                    0.0,
                ),
                "metadata": result.get(
                    "metadata",
                    {},
                ),
            }
            for result in retrieved_results
        ]

    def _classify(
        self,
        evidence: List[Dict[str, Any]],
    ) -> str:

        if not evidence:
            return "UNSUPPORTED"

        source_types = {
            item.get("source_type")
            for item in evidence
        }

        # Synthetic/test evidence can never establish a factual
        # literary relationship.
        if "synthetic_test" in source_types:
            return "INTERPRETATION"
        # A relationship can only be established when
        # literary evidence is actually present.
        if "tamil_rag" not in source_types:
            return "UNSUPPORTED"

        # Explicit relationship metadata may be supplied
        # by a validated upstream analysis component.
        explicit_types = []

        for item in evidence:
            metadata = item.get("metadata", {})

            if not isinstance(metadata, dict):
                continue

            relationship_type = metadata.get(
                "relationship_type"
            )

            if relationship_type in RELATIONSHIP_TYPES:
                explicit_types.append(
                    relationship_type
                )

        # Only accept explicitly supplied relationship types.
        if explicit_types:
            priority = [
                "FACT",
                "ANALOGY",
                "HYPOTHESIS",
                "INTERPRETATION",
                "UNSUPPORTED",
            ]

            for relationship_type in priority:
                if relationship_type in explicit_types:
                    return relationship_type

        # Literary evidence exists, but no validated
        # relationship classification was supplied.
        return "INTERPRETATION"

    def _confidence(
        self,
        relationship_type: str,
        evidence: List[Dict[str, Any]],
    ) -> float:

        if relationship_type == "UNSUPPORTED":
            return 0.0

        if relationship_type == "FACT":
            return 0.9

        if relationship_type == "INTERPRETATION":
            return 0.5

        if relationship_type == "ANALOGY":
            return 0.4

        if relationship_type == "HYPOTHESIS":
            return 0.25

        return 0.0

    def _reason(self, relationship_type: str) -> str:

        reasons = {
            "FACT": (
                "The relationship is explicitly supported by the "
                "available evidence."
            ),
            "INTERPRETATION": (
                "The available evidence permits a conceptual "
                "interpretation, but does not establish a scientific fact."
            ),
            "ANALOGY": (
                "The evidence indicates a structural or conceptual "
                "similarity rather than identity."
            ),
            "HYPOTHESIS": (
                "The proposed relationship is speculative and requires "
                "further investigation."
            ),
            "UNSUPPORTED": (
                "There is insufficient evidence to establish a meaningful "
                "relationship."
            ),
        }

        return reasons[relationship_type]

    def _unsupported(
        self,
        scientific_concepts: List[str],
        reason: str,
    ) -> Dict[str, Any]:

        return {
            "relationship_type": "UNSUPPORTED",
            "relationship_confidence": 0.0,
            "scientific_concepts": scientific_concepts,
            "evidence": [],
            "reason": reason,
        }