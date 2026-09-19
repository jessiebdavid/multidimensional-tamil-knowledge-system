from typing import Any, Dict

from processing.dimensions.base import DimensionProcessor


class ThreeDProcessor(DimensionProcessor):
    """Three-axis conceptual processing."""

    dimension = "3D"

    def process(self, concept: Dict[str, Any]) -> Dict[str, Any]:
        name = concept.get("name", "")
        keywords = concept.get("keywords", [])
        context_terms = concept.get("context_terms", [])

        axes = [
            name,
            keywords[0] if keywords else "property",
            context_terms[0] if context_terms else "context",
        ]

        return {
            "dimension": self.dimension,
            "concept": name,
            "representation_type": "three_axis_structure",
            "axes": axes,
            "properties": {
                "axis_count": 3,
                "keyword_count": len(keywords),
                "context_count": len(context_terms),
            },
        }