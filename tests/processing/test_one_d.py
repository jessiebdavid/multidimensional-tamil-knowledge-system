from processing.dimensions.one_d.processor import OneDProcessor


def test_one_d_processing():
    concept = {
        "name": "Time Dilation",
        "definition": "A relativistic effect in which elapsed time differs between observers.",
        "keywords": [
            "time",
            "relativity",
            "clock",
        ],
    }

    result = OneDProcessor().process(concept)

    assert result["dimension"] == "1D"
    assert result["concept"] == "Time Dilation"
    assert result["representation_type"] == "linear_scalar"
    assert result["primary_axis"] == "Time Dilation"
    assert result["properties"]["concept_present"] is True
    assert result["properties"]["definition_present"] is True
    assert result["properties"]["keyword_count"] == 3