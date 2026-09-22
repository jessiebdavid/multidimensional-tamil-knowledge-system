from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class Evidence:
    """
    Common evidence representation used by all retrieval sources.

    Retrieval evidence is descriptive only. It does not establish
    a scientific-literary relationship.
    """

    source_id: str
    source_type: str
    text: str

    retrieval_score: float = 0.0

    matched_terms: List[str] = field(default_factory=list)

    provenance: Dict[str, Any] = field(default_factory=dict)

    metadata: Dict[str, Any] = field(default_factory=dict)