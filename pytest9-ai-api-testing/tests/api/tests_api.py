"""API tests for the support triage system. """


import pytest

@pytest.mark.api
def test_create_ticket_returns_created_response(api_client):
    """Test that creating a ticket returns a 201 Created response."""
    response = api_client.post("/tickets", json={"message": "I was charged twice.   "}
                               )
    
    assert response.status_code == 201
    assert response.json() ["department"] == "billing"
