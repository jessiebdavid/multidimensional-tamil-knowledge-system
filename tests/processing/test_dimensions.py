from processing.dimensions.one_d.processor import OneDProcessor
from processing.dimensions.two_d.processor import TwoDProcessor
from processing.dimensions.three_d.processor import ThreeDProcessor
from processing.dimensions.four_d.processor import FourDProcessor


CONCEPT = {
    "name": "Time Dilation",
    "definition": "A relativistic effect involving differences in elapsed time.",
    "keywords": ["time", "relativity", "clock"],
    "context_terms": ["spacetime", "observer"],
}


def test_all_dimension_processors():
    processors = [
        OneDProcessor(),
        TwoDProcessor(),
        ThreeDProcessor(),
        FourDProcessor(),
    ]

    results = [
        processor.process(CONCEPT)
        for processor in processors
    ]

    assert [result["dimension"] for result in results] == [
        "1D",
        "2D",
        "3D",
        "4D",
    ]

    assert results[0]["representation_type"] == "linear_scalar"
    assert results[1]["representation_type"] == "two_axis_relationship"
    assert results[2]["representation_type"] == "three_axis_structure"
    assert results[3]["representation_type"] == "spatiotemporal_structure"

    assert results[1]["properties"]["axis_count"] == 2
    assert results[2]["properties"]["axis_count"] == 3
    assert results[3]["properties"]["axis_count"] == 4