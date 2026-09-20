from sentence_transformers import CrossEncoder


MODEL_NAME = "cross-encoder/mmarco-mMiniLMv2-L12-H384-v1"


class TamilReranker:
    def __init__(self, top_k: int = 5):
        self.top_k = top_k
        self.model = CrossEncoder(MODEL_NAME)

    def rerank(self, query: str, results):
        if not query.strip():
            return []

        if not results:
            return []

        pairs = [
            [query, result.text]
            for result in results
        ]

        scores = self.model.predict(pairs)

        ranked = []

        for result, score in zip(results, scores):
            result.retrieval_score = float(score)
            ranked.append(result)

        ranked.sort(
            key=lambda result: result.retrieval_score,
            reverse=True,
        )

        return ranked[:self.top_k]