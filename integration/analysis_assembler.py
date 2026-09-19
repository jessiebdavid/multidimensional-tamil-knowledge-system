from typing import Any, Dict, List

from shared.schemas.analysis_result import AnalysisResult


class AnalysisAssembler:
    """
    Combines scientific processing, dimensional analysis,
    Tamil retrieval evidence, and relationship analysis into
    the shared AnalysisResult contract.

    This component does not make new scientific or literary claims.
    """

    def assemble(
        self,
        scientific_query: Dict[str, Any],
        wormhole_result: Dict[str, Any],
        tamil_results: List[Dict[str, Any]],
        relationship_result: Dict[str, Any],
    ) -> AnalysisResult:

        concept_mapping = wormhole_result.get(
            "concept_mapping",
            {},
        )

        context_mapping = wormhole_result.get(
            "context_mapping",
            {},
        )

        dimension_route = wormhole_result.get(
            "dimension_route",
            {},
        )

        return AnalysisResult(
            scientific_concepts=concept_mapping.get(
                "all_concepts",
                [],
            ),
            scientific_domains=context_mapping.get(
                "domains",
                [],
            ),
            dimensional_analysis=dimension_route.get(
                "dimensional_analysis",
                [],
            ),
            tamil_evidence=tamil_results,
            relationship_type=relationship_result.get(
                "relationship_type",
                "UNSUPPORTED",
            ),
            relationship_confidence=relationship_result.get(
                "relationship_confidence",
                0.0,
            ),
            reasoning=relationship_result.get(
                "reason",
                "",
            ),
            uncertainty=(
                relationship_result.get(
                    "relationship_type",
                    "UNSUPPORTED",
                )
                != "FACT"
            ),
        )