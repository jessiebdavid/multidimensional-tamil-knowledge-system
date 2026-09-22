from dataclasses import dataclass, field
from typing import List


@dataclass
class QueryRoute:
    """
    Routing decision produced after query understanding.

    This describes where a query should go next.
    It does not perform retrieval itself.
    """

    scientific: bool = False
    tamil: bool = False
    research: bool = False

    requested_dimensions: List[str] = field(
        default_factory=list
    )

    intent: str = "GENERAL_QUERY"

    original_query: str = ""

    confidence: float = 0.0