from typing import Any, Dict, List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from scientific.query.llm_processor import LLMScientificQueryProcessor
from scientific.wormhole.router import WormholeRouter
from scientific.wormhole.tamil_bridge import ScientificToTamilBridge

from tamil_rag.interface.tamil_rag import TamilRAG

from processing.relationship.analyzer import RelationshipAnalyzer
from integration.analysis_assembler import AnalysisAssembler

from online_search.search_engine import OnlineSearchEngine


app = FastAPI(
    title="Multidimensional Tamil Knowledge System",
    version="0.1.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    query: str


class AnalyzeResponse(BaseModel):
    scientific_concepts: List[str]
    scientific_domains: List[str]
    dimensional_analysis: List[Dict[str, Any]]
    tamil_evidence: List[Dict[str, Any]]
    online_evidence: List[Dict[str, Any]]
    relationship_type: str
    relationship_confidence: float
    reasoning: str
    uncertainty: bool


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "multidimensional-tamil-knowledge-system",
    }


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest):

    # 1. Scientific query understanding using Tiny LLM
    processor = LLMScientificQueryProcessor()
    query = processor.process(request.query)

    # 2. Wormhole routing
    wormhole = WormholeRouter().route(query)

    # 3. Scientific -> Tamil retrieval request
    bridge = ScientificToTamilBridge()

    retrieval_request = bridge.build_request(
        query.__dict__,
        wormhole,
    )

    # 4. Real Tamil RAG
    tamil_results = TamilRAG(
        retrieval_top_k=10,
        final_top_k=5,
    ).retrieve(
        retrieval_request
    )

    tamil_dicts = [
        result.__dict__
        for result in tamil_results
    ]

    # 5. Online scientific evidence using Tavily
    search_query = " ".join(
        [
            request.query,
            *retrieval_request.scientific_concepts,
            *retrieval_request.scientific_domains,
        ]
    ).strip()

    online_results = OnlineSearchEngine().search(
        search_query,
        max_results=5,
    )

    online_dicts = [
        result.__dict__
        for result in online_results
    ]

    # 6. Relationship analysis
    relationship = RelationshipAnalyzer().analyze(
        scientific_concepts=retrieval_request.scientific_concepts,
        retrieved_results=tamil_dicts,
    )

    # 7. Final structured analysis
    result = AnalysisAssembler().assemble(
    scientific_query=query.__dict__,
    wormhole_result=wormhole,
    tamil_results=tamil_dicts,
    relationship_result=relationship,
    online_results=online_dicts,
)
    # 8. Add online evidence to final response
    result_dict = result.__dict__
    result_dict["online_evidence"] = online_dicts

    return AnalyzeResponse(
        **result_dict
    )