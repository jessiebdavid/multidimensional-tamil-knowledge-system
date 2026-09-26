from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class AnalysisResult:
    """
    Shared structured result produced after scientific processing,
    dimensional analysis, Tamil retrieval, and relationship analysis.

    This schema is an integration contract.
    """

    scientific_concepts: List[str] = field(
        default_factory=list
    )

    scientific_domains: List[str] = field(
        default_factory=list
    )

    dimensional_analysis: List[Dict[str, Any]] = field(
        default_factory=list
    )

    tamil_evidence: List[Dict[str, Any]] = field(
        default_factory=list
    )

    online_evidence: List[Dict[str, Any]] = field(
        default_factory=list
    )

    relationship_type: str = "UNSUPPORTED"

    relationship_confidence: float = 0.0

    reasoning: str = ""

    uncertainty: bool = True