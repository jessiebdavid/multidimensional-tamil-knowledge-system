# Multidimensional Tamil Knowledge System

## 1. Research Objective

Can computational methods identify meaningful conceptual relationships between scientific concepts and ideas expressed in classical Tamil literature?

The system must distinguish:

- FACT
- INTERPRETATION
- ANALOGY
- HYPOTHESIS

The system must never force a relationship when sufficient evidence is unavailable.

The system may return:

> No sufficiently relevant relationship was found.

---

## 2. High-Level Architecture

USER
  |
  v
QUERY HANDLER
  |
  v
TINY LLM
  |
  v
WORMHOLE
  |
  +----------------------+----------------------+
  |                                             |
  v                                             v
SCIENTIFIC KB                         TAMIL RAG
  |                                             |
  +----------------------+----------------------+
                         |
                         v
                  4D PROCESSING
                         |
                         v
              RELATIONSHIP ANALYSIS
                         |
                         v
               STRUCTURED ANALYSIS
                         |
                         v
              BACKEND INTEGRATION
                         |
                         v
                 FINAL LLM SYNTHESIS
                         |
                         v
                       UI/UX

---

## 3. Wormhole Architecture

The Wormhole is a computational architecture metaphor inspired by the conceptual idea of a physical wormhole.

It does not claim to reproduce physical wormhole behaviour.

The Wormhole consists of:

- `router.py`
- `concept_bridge.py`
- `context_mapper.py`
- `model_router.py`
- `dimension_router.py`

Its purpose is to connect scientific concepts and Tamil literary concepts through controlled computational transformations.

---

## 4. Scientific Intelligence Branch

The Scientific Intelligence branch is responsible for:

- Scientific knowledge base
- Scientific concept extraction
- Scientific concept classification
- Scientific keywords
- Scientific concept expansion
- Tiny/Small LLM
- Wormhole architecture
- Scientific-to-Tamil concept bridge
- Context routing
- Model routing
- Dimension routing
- Scientific integration preparation

---

## 5. Tamil RAG Branch

The Tamil RAG branch is responsible for:

- Tamil literary corpus
- Text preprocessing
- Embeddings
- Vector database / FAISS
- Retrieval
- Reranking
- Tamil retrieval results

---

## 6. Shared Components

Shared project-level contracts are stored under `shared/`.

```text
shared/
+---schemas/
|   +---scientific_query.py
|   +---tamil_retrieval.py
|   \---analysis_result.py
\---interfaces/
    \---tamil_retrieval.py
```

These contracts define how the Scientific Intelligence and Tamil RAG branches communicate.

---

## 7. Retrieval Score vs Relationship Confidence

Retrieval score and relationship confidence are separate concepts.

### Retrieval Score

Measures how strongly a retrieved Tamil passage matches the query.

### Relationship Confidence

Measures how strongly the system determines that a meaningful scientific-literary relationship exists.

Only the relationship analysis stage generates relationship confidence.

A retrieval score must never automatically become relationship confidence.

---

## 8. Mock RAG

A mock Tamil RAG implementation may be used to test the integration contract before the real Tamil RAG backend is available.

Mock records must be explicitly marked as synthetic/test records.

Mock data must never be presented as genuine literary evidence.

---

## 9. Dimensional Processing

The system will eventually process relationships through:

- 1D
- 2D
- 3D
- 4D

These dimensions represent computational analytical layers and must not be presented as unsupported claims about physical reality.

---

## 10. Final LLM

The Final LLM is a shared component.

It is responsible for synthesizing the structured outputs produced after the scientific and Tamil processing branches have been integrated.

It is not exclusively owned by the Scientific Intelligence branch.

---

## 11. UI/UX

UI/UX development is the final stage.

It begins only after:

1. Scientific backend is implemented.
2. Tamil RAG backend is implemented.
3. Both backends are integrated.
4. End-to-end testing succeeds.
5. Final LLM synthesis is integrated.

---

## 12. Development Order

The development sequence is frozen as:

1. Phase 0 - Architecture Freeze
2. Phase 1 - Repository Setup
3. Phase 2 - Scientific Knowledge Base
4. Phase 3 - Scientific Query Processing
5. Phase 4 - Tiny/Small LLM
6. Phase 5 - Wormhole
7. Phase 6 - Scientific  Tamil Concept Bridge
8. Phase 7 - Mock Tamil RAG
9. Phase 8 - 1D / 2D / 3D / 4D Processing
10. Phase 9 - Relationship Classification
11. Phase 10 - Integration Preparation
12. Phase 11 - Real Backend Integration
13. End-to-End Testing
14. Final LLM Synthesis
15. UI/UX
