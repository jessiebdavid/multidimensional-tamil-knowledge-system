from typing import List

from scientific.knowledge_base.retriever import (
    ScientificKBRetriever,
)
from shared.schemas.evidence import Evidence
from shared.schemas.retrieval import RetrievalRequest


class UnifiedRetriever:
    """
    Coordinates retrieval across available evidence sources.

    Each source is optional and controlled by RetrievalRequest.
    """

    def __init__(
        self,
        scientific_retriever=None,
        tamil_retriever=None,
        research_retriever=None,
    ):
        self.scientific_retriever = (
            scientific_retriever
            or ScientificKBRetriever()
        )
        self.tamil_retriever = tamil_retriever
        self.research_retriever = research_retriever

    def retrieve(
        self,
        request: RetrievalRequest,
    ) -> List[Evidence]:

        evidence = []

        if request.retrieve_scientific:
            scientific_terms = (
                request.scientific_concepts
                + request.scientific_domains
                + request.context_terms
            )

            evidence.extend(
                self.scientific_retriever.retrieve(
                    scientific_terms,
                    top_k=request.top_k,
                )
            )

        if request.retrieve_tamil and self.tamil_retriever:
            tamil_results = self.tamil_retriever.retrieve(
                scientific_concepts=request.scientific_concepts,
                scientific_domains=request.scientific_domains,
                context_terms=request.context_terms,
                query_terms=request.context_terms,
                top_k=request.top_k,
            )

            evidence.extend(tamil_results)

        if request.retrieve_research and self.research_retriever:
            research_results = self.research_retriever.retrieve(
                query=request.query,
                scientific_concepts=request.scientific_concepts,
                context_terms=request.context_terms,
                top_k=request.top_k,
            )

            evidence.extend(research_results)

        evidence.sort(
            key=lambda item: item.retrieval_score,
            reverse=True,
        )

        return evidence[:request.top_k]