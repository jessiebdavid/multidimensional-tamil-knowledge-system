from abc import ABC, abstractmethod
from typing import Any, Dict


class DimensionProcessor(ABC):
    """
    Base interface for dimensional processing.

    Each dimensional processor receives a structured scientific concept
    and returns a standardized dimensional representation.

    This layer performs computational representation only.
    It does not determine literary relationships or scientific truth.
    """

    dimension: str

    @abstractmethod
    def process(
        self,
        concept: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Process a scientific concept under the processor's dimension.
        """
        raise NotImplementedError