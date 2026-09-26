import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List

from dotenv import load_dotenv
from tavily import TavilyClient


load_dotenv()


@dataclass
class SearchResult:
    """
    Represents one piece of evidence retrieved from an online source.
    """
    title: str
    url: str
    snippet: str
    source: str
    retrieved_at: str


class OnlineSearchEngine:
    """
    Tavily-based online scientific search engine.
    """

    def __init__(self):
        api_key = os.getenv("TAVILY_API_KEY")

        if not api_key:
            raise ValueError(
                "TAVILY_API_KEY was not found. "
                "Add it to the .env file."
            )

        self.client = TavilyClient(api_key=api_key)

    def search(
        self,
        query: str,
        max_results: int = 5,
    ) -> List[SearchResult]:

        if not isinstance(query, str):
            raise TypeError("query must be a string.")

        query = query.strip()

        if not query:
            raise ValueError("query cannot be empty.")

        if max_results <= 0:
            raise ValueError("max_results must be greater than 0.")

        response = self.client.search(
            query=query,
            search_depth="advanced",
            max_results=max_results,
        )

        retrieved_at = self._retrieved_at()

        results = []

        for item in response.get("results", []):
            results.append(
                SearchResult(
                    title=item.get("title", ""),
                    url=item.get("url", ""),
                    snippet=item.get("content", ""),
                    source=item.get("url", ""),
                    retrieved_at=retrieved_at,
                )
            )

        return results

    @staticmethod
    def _retrieved_at() -> str:
        return datetime.now(timezone.utc).isoformat()