from typing import List

from shared.schemas.evidence import Evidence


class ResearchRetriever:
    """
    Interface for research/web evidence retrieval.

    This stage does not perform live web retrieval yet.
    It defines the contract that a real research backend
    can implement later.
    """

    def retrieve(
        self,
        query: str,
        scientific_concepts: List[str],
        context_terms: List[str],
        top_k: int = 5,
    ) -> List[Evidence]:
        raise NotImplementedError