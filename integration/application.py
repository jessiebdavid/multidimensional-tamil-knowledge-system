from integration.analysis_pipeline import AnalysisPipeline
from scientific.query.handler import QueryHandler


class ScientificApplication:
    """
    Application-level entry point for the scientific analysis pipeline.

    Converts a raw user query into InputUnderstanding and then
    executes the structured analysis pipeline.
    """

    def __init__(
        self,
        query_handler=None,
        analysis_pipeline=None,
    ):
        self.query_handler = (
            query_handler or QueryHandler()
        )
        self.analysis_pipeline = (
            analysis_pipeline or AnalysisPipeline()
        )

    def analyze(self, query: str):
        understanding = self.query_handler.understand(query)

        scientific_concepts = []

        if understanding.primary_concept:
            scientific_concepts.append(
                understanding.primary_concept
            )

        scientific_concepts.extend(
            understanding.related_concepts
        )

        return self.analysis_pipeline.analyze(
            query=query,
            scientific_concepts=scientific_concepts,
            scientific_domains=(
                [understanding.scientific_domain]
                if understanding.scientific_domain
                else []
            ),
            context_terms=understanding.context_terms,
            retrieve_tamil=(
                understanding.requires_tamil_retrieval
            ),
            retrieve_research=(
                understanding.requires_research
            ),
        )