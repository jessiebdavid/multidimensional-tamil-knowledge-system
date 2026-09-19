from typing import Any, Dict

from processing.dimensions.base import DimensionProcessor


class TwoDProcessor(DimensionProcessor):
    """Two-dimensional conceptual relationship processing."""

    dimension = "2D"

    def process(self, concept: Dict[str, Any]) -> Dict[str, Any]:
        name = concept.get("name", "")
        keywords = concept.get("keywords", [])

        axis_a = name
        axis_b = keywords[0] if keywords else "context"

        return {
            "dimension": self.dimension,
            "concept": name,
            "representation_type": "two_axis_relationship",
            "axes": {
                "axis_a": axis_a,
                "axis_b": axis_b,
            },
            "properties": {
                "axis_count": 2,
                "keyword_count": len(keywords),
            },
        }