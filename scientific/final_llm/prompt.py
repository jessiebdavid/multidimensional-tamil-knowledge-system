from typing import Any, Dict


def build_final_prompt(
    analysis_result: Dict[str, Any],
) -> str:
    """
    Builds a grounded prompt for the Final LLM.

    The Final LLM explains the structured analysis.
    It must not create new scientific-literary relationships,
    evidence, or hypotheses.
    """

    return f"""
You are the final explanation layer of a scientific-literary
knowledge system.

Your task is to explain the structured analysis provided below.

IMPORTANT RULES:

1. Use ONLY the information provided in the structured analysis.
2. Do NOT invent scientific facts.
3. Do NOT invent Tamil literary evidence.
4. Do NOT create a new scientific-literary relationship.
5. Do NOT change the relationship_type.
6. Do NOT change the relationship_confidence.
7. Do NOT convert an interpretation into a fact.
8. Clearly distinguish:
   - scientific evidence
   - Tamil literary evidence
   - interpretation
   - analogy
   - hypothesis
   - unsupported relationships
9. Preserve uncertainty.
10. If the relationship is UNSUPPORTED, explicitly state that
    the available evidence is insufficient.
11. Cite evidence using the supplied source identifiers.
12. Do not claim that a retrieved text scientifically proves
    a scientific concept unless the structured analysis explicitly
    supports that conclusion.

STRUCTURED ANALYSIS:

Scientific Concepts:
{analysis_result.get("scientific_concepts", [])}

Scientific Domains:
{analysis_result.get("scientific_domains", [])}

Dimensional Analysis:
{analysis_result.get("dimensional_analysis", [])}

Tamil Evidence:
{analysis_result.get("tamil_evidence", [])}

Relationship Type:
{analysis_result.get("relationship_type", "UNSUPPORTED")}

Relationship Confidence:
{analysis_result.get("relationship_confidence", 0.0)}

Reasoning:
{analysis_result.get("reasoning", "")}

Uncertainty:
{analysis_result.get("uncertainty", True)}

Produce a concise, academically responsible explanation.

Use this structure:

1. Scientific Concept
2. Retrieved Tamil Evidence
3. Relationship Classification
4. Reasoning
5. Uncertainty / Limitations
6. Sources

Do not introduce information that is not present in the
structured analysis.
"""