from dataclasses import dataclass, field
from typing import List


@dataclass
class QueryIntent:
    """
    Structured representation of what the user is asking.

    Intent classification determines which retrieval and
    analysis capabilities should be activated.
    """

    intent: str
    original_query: str

    target_text: str = ""

    scientific_requested: bool = False
    tamil_requested: bool = False
    research_requested: bool = False
    dimensional_requested: bool = False

    requested_dimensions: List[str] = field(
        default_factory=list
    )

    translation_requested: bool = False
    comparison_requested: bool = False

    confidence: float = 0.0