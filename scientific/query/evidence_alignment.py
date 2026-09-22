from typing import List

from shared.schemas.evidence import Evidence
from shared.schemas.evidence_alignment import EvidenceAlignment


class EvidenceAligner:
    """
    Groups unified evidence by source type.

    No relationship or confidence decision is made here.
    """

    def align(
        self,
        evidence: List[Evidence],
        required_sources: List[str] | None = None,
    ) -> EvidenceAlignment:

        scientific = []
        tamil = []
        research = []

        for item in evidence:
            if item.source_type == "scientific_kb":
                scientific.append(item)

            elif item.source_type == "tamil_rag":
                tamil.append(item)

            elif item.source_type == "research":
                research.append(item)

        present = set()

        if scientific:
            present.add("scientific_kb")

        if tamil:
            present.add("tamil_rag")

        if research:
            present.add("research")

        missing = []

        for source in required_sources or []:
            if source not in present:
                missing.append(source)

        return EvidenceAlignment(
            scientific_evidence=scientific,
            tamil_evidence=tamil,
            research_evidence=research,
            missing_sources=missing,
        )