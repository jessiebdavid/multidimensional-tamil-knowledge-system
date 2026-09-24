from shared.schemas.tamil_retrieval import TamilRetrievalRequest
from tamil_rag.interface.tamil_rag import TamilRAG


def test_tamil_rag_returns_list():
    rag = TamilRAG(
        retrieval_top_k=10,
        final_top_k=5,
    )

    request = TamilRetrievalRequest(
        query_terms=["அறிவு"],
        retrieval_reason="Test Tamil RAG interface",
    )

    results = rag.retrieve(request)

    assert isinstance(results, list)


def test_tamil_rag_empty_query_returns_no_results():
    rag = TamilRAG(
        retrieval_top_k=10,
        final_top_k=5,
    )

    request = TamilRetrievalRequest()

    results = rag.retrieve(request)

    assert results == []


def test_tamil_rag_respects_final_top_k():
    rag = TamilRAG(
        retrieval_top_k=10,
        final_top_k=2,
    )

    request = TamilRetrievalRequest(
        query_terms=["அறிவு"],
        retrieval_reason="Test final top-k",
    )

    results = rag.retrieve(request)

    assert len(results) <= 2


def test_tamil_rag_result_structure():
    rag = TamilRAG(
        retrieval_top_k=10,
        final_top_k=5,
    )

    request = TamilRetrievalRequest(
        query_terms=["அறிவு"],
        retrieval_reason="Test result structure",
    )

    results = rag.retrieve(request)

    if not results:
        return

    result = results[0]

    assert isinstance(result.source_id, str)
    assert isinstance(result.source_type, str)
    assert isinstance(result.text, str)
    assert isinstance(result.matched_terms, list)
    assert isinstance(result.retrieval_score, float)
    assert isinstance(result.metadata, dict)