from integration.analysis_pipeline import AnalysisPipeline
from scientific.query.handler import QueryHandler
from scientific.query.retrieval import UnifiedRetriever
from scientific.query.tamil_retrieval_adapter import TamilRAGAdapter
from tamil_rag.interface.tamil_rag import TamilRAG


class ScientificApplication:
    """
    End-to-end application entry point.

    Uses the real Tamil RAG when available.
    """

    def __init__(
        self,
        query_handler=None,
        analysis_pipeline=None,
    ):
        self.query_handler = (
            query_handler or QueryHandler()
        )

        if analysis_pipeline is None:
            tamil_rag = TamilRAG(
                retrieval_top_k=10,
                final_top_k=5,
            )

            tamil_adapter = TamilRAGAdapter(
                tamil_rag
            )

            retriever = UnifiedRetriever(
                tamil_retriever=tamil_adapter
            )

            analysis_pipeline = AnalysisPipeline(
                retriever=retriever
            )

        self.analysis_pipeline = analysis_pipeline

    def analyze(self, query: str):
        understanding = self.query_handler.understand(
            query
        )

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