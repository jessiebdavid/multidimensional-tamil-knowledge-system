from dataclasses import dataclass, field
from typing import List


@dataclass
class RelationshipResult:
    relationship_type: str
    confidence: float = 0.0

    scientific_evidence_ids: List[str] = field(
        default_factory=list
    )

    tamil_evidence_ids: List[str] = field(
        default_factory=list
    )

    research_evidence_ids: List[str] = field(
        default_factory=list
    )

    explanation: str = ""

    uncertainty: List[str] = field(
        default_factory=list
    )