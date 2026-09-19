from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class ScientificQuery:
    """
    Structured representation of a user's scientific query.

    This schema is the shared contract between scientific query
    processing and later stages of the system.
    """

    original_query: str
    normalized_query: str
    concepts: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    domains: List[str] = field(default_factory=list)
    context_terms: List[str] = field(default_factory=list)
    expanded_concepts: List[Dict[str, Any]] = field(default_factory=list)