"""Tests for AI-related API functionality."""

import pytest

@pytest.mark.ai 
@pytest.mark.live
def test_live_model_response_has_expected_shape(model_client):
    """Test that the live model response has the expected shape."""
    response = model_client.classify("I was charged twice.")
    
    assert response.labels in ["billing", "technical", "account"]
    assert 0 <= response.confidence <= 1
