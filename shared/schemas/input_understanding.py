from dataclasses import dataclass, field
from typing import List


@dataclass
class InputUnderstanding:
    original_query: str

    primary_concept: str = ""

    scientific_domain: str = ""

    query_type: str = "GENERAL_QUERY"

    related_concepts: List[str] = field(
        default_factory=list
    )

    context_terms: List[str] = field(
        default_factory=list
    )

    target_text: str = ""

    requires_tamil_retrieval: bool = False

    requires_research: bool = False

    requested_dimensions: List[str] = field(
        default_factory=list
    )

    uncertainty: List[str] = field(
        default_factory=list
    )

    source: str = "deterministic"