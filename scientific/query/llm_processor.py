from typing import Any, Dict

from scientific.tiny_llm.qwen_model import QwenTinyLLM
from shared.schemas.scientific_query import ScientificQuery


class LLMScientificQueryProcessor:
    """
    Uses the Tiny LLM to interpret an arbitrary user question and
    converts the interpretation into the existing ScientificQuery
    contract used by the Wormhole and downstream pipeline.
    """

    def __init__(self):
        self.llm = QwenTinyLLM()

    def process(self, query: str) -> ScientificQuery:
        """
        Interpret a raw user question using the Tiny LLM.
        """

        if not isinstance(query, str):
            raise TypeError("query must be a string.")

        query = query.strip()

        if not query:
            raise ValueError("query cannot be empty.")

        interpretation: Dict[str, Any] = self.llm.interpret(
            query
        )

        primary_concept = interpretation.get(
            "primary_concept"
        )

        relevant_concepts = interpretation.get(
            "relevant_concepts",
            [],
        )

        scientific_domains = interpretation.get(
            "scientific_domains",
            [],
        )

        relevant_context = interpretation.get(
            "relevant_context",
            [],
        )

        concepts = []

        if primary_concept:
            concepts.append(primary_concept)

        for concept in relevant_concepts:
            if concept and concept not in concepts:
                concepts.append(concept)

        keywords = list(concepts)

        normalized_query = " ".join(
            query.split()
        )

        return ScientificQuery(
            original_query=query,
            normalized_query=normalized_query,
            concepts=concepts,
            keywords=keywords,
            domains=scientific_domains,
            context_terms=relevant_context,
            expanded_concepts=[],
        )