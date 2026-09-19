import json
import re
from pathlib import Path
from scientific.query.expander import ScientificConceptExpander

from shared.schemas.scientific_query import ScientificQuery


class ScientificQueryProcessor:
    """
    Converts a raw user query into a structured ScientificQuery.

    Uses the scientific knowledge base for deterministic concept
    matching while avoiding overly broad matches from generic terms.
    """

    def __init__(self, knowledge_base_path: str | Path):
        self.knowledge_base_path = Path(knowledge_base_path)
        self.knowledge_base = self._load_knowledge_base()
        self.expander = ScientificConceptExpander(
            self.knowledge_base_path
        )

    def _load_knowledge_base(self) -> dict:
        with self.knowledge_base_path.open(
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    def normalize(self, query: str) -> str:
        """Normalize whitespace and casing."""
        query = query.strip().lower()
        query = re.sub(r"\s+", " ", query)

        query = re.sub(r"\bfields\b", "fields", query)
        query = re.sub(r"\bforces\b", "forces", query)
        query = re.sub(r"\bwaves\b", "wave",query)
        query = re.sub(r"\bparticles\b", "particle",query)
        query = re.sub(r"\boscillations\b", "oscillations",query)

        return query

    def _contains_phrase(self, query: str, phrase: str) -> bool:
        """
        Check whether a phrase occurs as a meaningful word sequence.
        """
        phrase = phrase.strip().lower()

        if not phrase:
            return False

        pattern = r"\b" + re.escape(phrase) + r"\b"
        return re.search(pattern, query) is not None

    def process(self, query: str) -> ScientificQuery:
        normalized_query = self.normalize(query)

        concepts = []
        keywords = []
        domains = []
        context_terms = []

        for domain in self.knowledge_base.get("domains", []):
            domain_name = domain.get("name", "")

            for subdomain in domain.get("subdomains", []):
                subdomain_name = subdomain.get("name", "")

                for concept in subdomain.get("concepts", []):
                    concept_name = concept.get("name", "")
                    concept_keywords = concept.get("keywords", [])
                    concept_context = concept.get("context_terms", [])

                    # Strong match: exact concept name.
                    concept_match = self._contains_phrase(
                        normalized_query,
                        concept_name
                    )

                    if concept_match:
                        if concept_name not in concepts:
                            concepts.append(concept_name)

                        if domain_name and domain_name not in domains:
                            domains.append(domain_name)

                        if subdomain_name and subdomain_name not in domains:
                            domains.append(subdomain_name)

                        for keyword in concept_keywords:
                            if keyword not in keywords:
                                keywords.append(keyword)

                        for term in concept_context:
                            if term not in context_terms:
                                context_terms.append(term)

                        continue

                    # Conservative keyword matching.
                    #
                    # Only use keywords containing at least two words.
                    # This prevents generic words such as "time",
                    # "rate", "field", "space", etc. from triggering
                    # unrelated concepts.
                    meaningful_keywords = [
                        keyword
                        for keyword in concept_keywords
                        if len(keyword.split()) >= 2
                    ]

                    matched_keyword = any(
                        self._contains_phrase(
                            normalized_query,
                            keyword
                        )
                        for keyword in meaningful_keywords
                    )

                    if matched_keyword:
                        if concept_name not in concepts:
                            concepts.append(concept_name)

                        if domain_name and domain_name not in domains:
                            domains.append(domain_name)

                        if subdomain_name and subdomain_name not in domains:
                            domains.append(subdomain_name)

                        for keyword in concept_keywords:
                            if keyword not in keywords:
                                keywords.append(keyword)

                        for term in concept_context:
                            if term not in context_terms:
                                context_terms.append(term)

        expanded_concepts = self.expander.expand(concepts)

        return ScientificQuery(
            original_query=query,
            normalized_query=normalized_query,
            concepts=concepts,
            keywords=keywords,
            domains=domains,
            context_terms=context_terms,
            expanded_concepts=expanded_concepts,
        )