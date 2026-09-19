from typing import Any, Dict

from processing.dimensions.four_d.processor import FourDProcessor
from processing.dimensions.one_d.processor import OneDProcessor
from processing.dimensions.three_d.processor import ThreeDProcessor
from processing.dimensions.two_d.processor import TwoDProcessor


class DimensionRouter:
    """
    Routes scientific concepts to the appropriate dimensional processor.

    The router uses dimensional metadata from the scientific knowledge base.
    It does not invent dimensional claims.
    """

    def __init__(self):
        self.processors = {
            "1D": OneDProcessor(),
            "2D": TwoDProcessor(),
            "3D": ThreeDProcessor(),
            "4D": FourDProcessor(),
        }

    def route(
        self,
        scientific_query: Dict[str, Any],
        model_result: Dict[str, Any],
    ) -> Dict[str, Any]:
        expanded_concepts = scientific_query.get(
            "expanded_concepts",
            [],
        )

        routed_dimensions = []
        dimensional_analysis = []

        for concept in expanded_concepts:
            dimensions = concept.get(
                "dimensions",
                {},
            )

            supported = dimensions.get(
                "supported",
                [],
            )

            for dimension in supported:
                processor = self.processors.get(dimension)

                if processor is None:
                    continue

                routed_dimensions.append(dimension)

                dimensional_analysis.append(
                    processor.process(concept)
                )

        routed_dimensions = list(dict.fromkeys(routed_dimensions))

        if not expanded_concepts:
            return {
                "status": "unresolved",
                "dimensions": [],
                "dimensional_analysis": [],
                "dimension_count": 0,
            }

        return {
            "status": "resolved",
            "dimensions": routed_dimensions,
            "dimensional_analysis": dimensional_analysis,
            "dimension_count": len(routed_dimensions),
        }