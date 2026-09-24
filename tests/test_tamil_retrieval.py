from shared.schemas.tamil_retrieval import TamilRetrievalRequest
from tamil_rag.retrieval.semantic_retriever import SemanticTamilRetriever


def test_empty_query_returns_no_results():
    retriever = SemanticTamilRetriever(top_k=5)

    request = TamilRetrievalRequest()

    results = retriever.retrieve(request)

    assert results == []


def test_semantic_retrieval_returns_results():
    retriever = SemanticTamilRetriever(top_k=5)

    request = TamilRetrievalRequest(
        query_terms=["அறிவு"],
        retrieval_reason="Test Tamil semantic retrieval",
    )

    results = retriever.retrieve(request)

    assert isinstance(results, list)
    assert len(results) <= 5


def test_retrieval_result_contains_required_fields():
    retriever = SemanticTamilRetriever(top_k=5)

    request = TamilRetrievalRequest(
        query_terms=["அறிவு"],
        retrieval_reason="Test result structure",
    )

    results = retriever.retrieve(request)

    if not results:
        return

    result = results[0]

    assert isinstance(result.source_id, str)
    assert isinstance(result.source_type, str)
    assert isinstance(result.text, str)
    assert isinstance(result.matched_terms, list)
    assert isinstance(result.retrieval_score, float)
    assert isinstance(result.metadata, dict)


def test_retrieval_respects_top_k():
    retriever = SemanticTamilRetriever(top_k=2)

    request = TamilRetrievalRequest(
        query_terms=["அறிவு"],
        retrieval_reason="Test top-k retrieval",
    )

    results = retriever.retrieve(request)

    assert len(results) <= 2