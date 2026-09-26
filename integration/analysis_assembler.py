from typing import Any, Dict, List

from shared.schemas.analysis_result import AnalysisResult


class AnalysisAssembler:
    """
    Assembles the final structured analysis result.

    This keeps scientific processing, Tamil evidence,
    online evidence, and relationship analysis in one
    shared result contract.
    """

    def assemble(
        self,
        scientific_query: Dict[str, Any],
        wormhole_result: Dict[str, Any],
        tamil_results: List[Dict[str, Any]],
        relationship_result: Dict[str, Any],
        online_results: List[Dict[str, Any]] | None = None,
    ) -> AnalysisResult:

        concept_mapping = wormhole_result.get(
            "concept_mapping", {}
        )

        context_mapping = wormhole_result.get(
            "context_mapping", {}
        )

        dimension_route = wormhole_result.get(
            "dimension_route", {}
        )

        return AnalysisResult(
            scientific_concepts=concept_mapping.get(
                "all_concepts", []
            ),

            scientific_domains=context_mapping.get(
                "domains", []
            ),

            dimensional_analysis=dimension_route.get(
                "dimensional_analysis", []
            ),

            tamil_evidence=tamil_results,

            online_evidence=online_results or [],

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