from integration.analysis_pipeline import AnalysisPipeline


def test_analysis_pipeline_with_scientific_evidence():

    pipeline = AnalysisPipeline()

    result = pipeline.analyze(
        query="What is time dilation?",
        scientific_concepts=[
            "Time Dilation",
        ],
        scientific_domains=[
            "Physics",
        ],
        context_terms=[
            "relativity",
            "clock",
        ],
    )

    assert "Time Dilation" in result.scientific_concepts
    assert "Physics" in result.scientific_domains
    assert len(result.dimensional_analysis) == 4
    assert result.relationship_type == "UNSUPPORTED"
    assert result.relationship_confidence == 0.0
    assert result.uncertainty is True