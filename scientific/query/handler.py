from shared.schemas.query_handler import QueryRoute
from scientific.query.intent import QueryIntentClassifier


class QueryHandler:
    """
    First-stage query orchestration layer.

    Responsibilities:
    1. Receive the raw user query.
    2. Determine the user's intent.
    3. Determine which knowledge domains are required.
    4. Produce a routing decision.

    The QueryHandler does NOT perform retrieval.
    """

    def __init__(
        self,
        intent_classifier=None,
    ):
        self.intent_classifier = (
            intent_classifier
            or QueryIntentClassifier()
        )

    def handle(
        self,
        query: str,
    ) -> QueryRoute:

        intent = self.intent_classifier.classify(
            query
        )

        return QueryRoute(
            scientific=intent.scientific_requested,
            tamil=intent.tamil_requested,
            research=intent.research_requested,
            requested_dimensions=list(
                intent.requested_dimensions
            ),
            intent=intent.intent,
            original_query=intent.original_query,
            confidence=intent.confidence,
        )