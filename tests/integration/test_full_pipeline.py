from scientific.query.processor import ScientificQueryProcessor
from scientific.wormhole.router import WormholeRouter
from scientific.wormhole.tamil_bridge import ScientificToTamilBridge

from tamil_rag.interface.tamil_rag import TamilRAG

from processing.relationship.analyzer import RelationshipAnalyzer
from integration.analysis_assembler import AnalysisAssembler


KNOWLEDGE_BASE = "data/scientific/scientific_knowledge.json"


def test_full_scientific_pipeline():

    # 1. Scientific query processing
    processor = ScientificQueryProcessor(KNOWLEDGE_BASE)

    query = processor.process(
        "What is time dilation?"
    )

    assert "Time Dilation" in query.concepts

    # 2. Wormhole routing
    wormhole = WormholeRouter().route(query)

    assert wormhole["model_route"]["status"] == "resolved"
    assert wormhole["dimension_route"]["status"] == "resolved"

    # 3. Scientific → Tamil retrieval request
    bridge = ScientificToTamilBridge()

    retrieval_request = bridge.build_request(
        query.__dict__,
        wormhole,
    )

    assert retrieval_request.scientific_concepts

    # 4. Real Tamil RAG
    tamil_results = TamilRAG(
        retrieval_top_k=10,
        final_top_k=5,
    ).retrieve(
        retrieval_request
    )

    assert len(tamil_results) > 0

    # Convert dataclasses to dictionaries
    tamil_dicts = [
        result.__dict__
        for result in tamil_results
    ]

    # 5. Relationship analysis
    relationship = RelationshipAnalyzer().analyze(
        scientific_concepts=retrieval_request.scientific_concepts,
        retrieved_results=tamil_dicts,
    )

    assert relationship["relationship_type"] == "INTERPRETATION"

    # 6. Final structured analysis
    result = AnalysisAssembler().assemble(
        scientific_query=query.__dict__,
        wormhole_result=wormhole,
        tamil_results=tamil_dicts,
        relationship_result=relationship,
    )

    # 7. Validate final contract
    assert result.scientific_concepts
    assert result.scientific_domains
    assert result.dimensional_analysis
    assert result.tamil_evidence

    assert result.relationship_type == "INTERPRETATION"

    assert 0.0 <= result.relationship_confidence <= 1.0