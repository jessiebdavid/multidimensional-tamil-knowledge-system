from dataclasses import dataclass, field
from typing import List


@dataclass
class TamilRetrievalRequest:
    """
    Shared contract for requesting Tamil-literature retrieval.

    This schema is the boundary between the scientific branch
    and the Tamil RAG branch.

    It describes what the Tamil retrieval system should search for.
    It does not contain retrieved literary evidence.
    """

    scientific_concepts: List[str] = field(default_factory=list)
    scientific_domains: List[str] = field(default_factory=list)
    context_terms: List[str] = field(default_factory=list)
    query_terms: List[str] = field(default_factory=list)

    retrieval_reason: str = ""


@dataclass
class TamilRetrievalResult:
    """
    Shared contract for Tamil-literature retrieval results.

    This represents retrieval output only. It must not contain
    relationship confidence or a claim that a literary item
    corresponds to a scientific concept.
    """

    source_id: str
    source_type: str
    text: str
    matched_terms: List[str] = field(default_factory=list)
    retrieval_score: float = 0.0
    metadata: dict = field(default_factory=dict)