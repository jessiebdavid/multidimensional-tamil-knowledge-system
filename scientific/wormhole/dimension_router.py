from typing import Any, Dict, List


class DimensionRouter:
    """
    Prepares dimensional routing metadata for downstream processing.

    This component does not perform 1D/2D/3D/4D analysis.
    Actual dimensional processing belongs to Phase 8.

    Dimensions are only routed when they are explicitly supplied
    by the scientific knowledge/query pipeline.
    """

    SUPPORTED_DIMENSIONS = ("1D", "2D", "3D", "4D")

    def route(
        self,
        scientific_query: Dict[str, Any],
        model_result: Dict[str, Any],
    ) -> Dict[str, Any]:
        expanded_concepts = scientific_query.get(
            "expanded_concepts",
            [],
        )

        dimensions = self._extract_dimensions(
            expanded_concepts
        )

        if dimensions:
            return {
                "status": "resolved",
                "dimensions": dimensions,
                "processing_stage": "phase_8",
                "reason": (
                    "Dimensional metadata was supplied by "
                    "the scientific knowledge pipeline."
                ),
            }

        return {
            "status": "unresolved",
            "dimensions": [],
            "processing_stage": "phase_8",
            "reason": (
                "No explicit dimensional metadata was "
                "available for this query."
            ),
        }

    def _extract_dimensions(
        self,
        expanded_concepts: List[Dict[str, Any]],
    ) -> List[str]:
        dimensions = []

        for concept in expanded_concepts:
            dimension_data = concept.get("dimensions", {})

            if not isinstance(dimension_data, dict):
                continue

            supported = dimension_data.get("supported", [])

            if not isinstance(supported, list):
                continue

            for dimension in supported:
                if (
                    isinstance(dimension, str)
                    and dimension in self.SUPPORTED_DIMENSIONS
                    and dimension not in dimensions
                ):
                    dimensions.append(dimension)

        return dimensions