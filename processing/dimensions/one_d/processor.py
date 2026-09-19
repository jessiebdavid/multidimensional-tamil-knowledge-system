from typing import Any, Dict

from processing.dimensions.base import DimensionProcessor


class OneDProcessor(DimensionProcessor):
    """
    One-dimensional conceptual processing.

    1D processing represents a scientific concept along a single
    conceptual axis. It does not claim that the underlying phenomenon
    is physically one-dimensional.
    """

    dimension = "1D"

    def process(
        self,
        concept: Dict[str, Any],
    ) -> Dict[str, Any]:
        name = concept.get("name", "")
        definition = concept.get("definition", "")
        keywords = concept.get("keywords", [])

        return {
            "dimension": self.dimension,
            "concept": name,
            "representation_type": "linear_scalar",
            "primary_axis": name,
            "definition": definition,
            "keywords": keywords,
            "properties": {
                "concept_present": bool(name),
                "definition_present": bool(definition),
                "keyword_count": len(keywords),
            },
        }