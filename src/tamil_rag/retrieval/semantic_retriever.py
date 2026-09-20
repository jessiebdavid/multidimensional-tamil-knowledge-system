from pathlib import Path
import json

import numpy as np
from sentence_transformers import SentenceTransformer

from shared.schemas.tamil_retrieval import (
    TamilRetrievalRequest,
    TamilRetrievalResult,
)
from shared.interfaces.tamil_retrieval import TamilRetrievalInterface


BASE_DIR = Path(__file__).resolve().parents[3]

EMBEDDING_FILE = (
    BASE_DIR / "indexes" / "tamil" / "embeddings.npy"
)

METADATA_FILE = (
    BASE_DIR / "indexes" / "tamil" / "metadata.json"
)

MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"


class SemanticTamilRetriever(TamilRetrievalInterface):

    def __init__(self, top_k: int = 5):
        self.top_k = top_k

        self.embeddings = np.load(EMBEDDING_FILE)

        with open(METADATA_FILE, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)

        self.model = SentenceTransformer(MODEL_NAME)

    def _build_query(
        self,
        request: TamilRetrievalRequest,
    ) -> str:

        terms = (
            request.scientific_concepts
            + request.scientific_domains
            + request.context_terms
            + request.query_terms
        )

        return " ".join(
            term.strip()
            for term in terms
            if isinstance(term, str) and term.strip()
        )

    def _find_matched_terms(
        self,
        request: TamilRetrievalRequest,
        text: str,
    ) -> list[str]:

        terms = (
            request.scientific_concepts
            + request.scientific_domains
            + request.context_terms
            + request.query_terms
        )

        matched_terms = []

        for term in terms:
            if not isinstance(term, str):
                continue

            term = term.strip()

            if term and term in text and term not in matched_terms:
                matched_terms.append(term)

        return matched_terms

    def retrieve(
        self,
        request: TamilRetrievalRequest,
    ) -> list[TamilRetrievalResult]:

        query = self._build_query(request)

        if not query:
            return []

        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True,
        )[0]

        scores = self.embeddings @ query_embedding

        top_indices = np.argsort(scores)[::-1][:self.top_k]

        results = []

        for index in top_indices:

            document = self.metadata[index]

            matched_terms = self._find_matched_terms(
                request,
                document["text"],
            )

            result = TamilRetrievalResult(
                source_id=document["source_id"],
                source_type=document["source_type"],
                text=document["text"],
                matched_terms=matched_terms,
                retrieval_score=float(scores[index]),
                metadata=document["metadata"],
            )

            results.append(result)

        return results


if __name__ == "__main__":

    retriever = SemanticTamilRetriever(top_k=5)

    request = TamilRetrievalRequest(
        query_terms=["அறிவு"],
        retrieval_reason="Direct semantic retrieval test",
    )

    results = retriever.retrieve(request)

    print("Results:", len(results))

    for result in results:
        print("\nSource ID:", result.source_id)
        print("Source type:", result.source_type)
        print("Matched terms:", result.matched_terms)
        print("Score:", result.retrieval_score)
        print("Text:", result.text)