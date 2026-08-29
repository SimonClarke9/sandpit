"""API tests for the support triage system. """


import pytest


from support_triage.services.ticket_router import (
    ClassificationResult, 
    TicketRouter    )   

class FakeModelClient:
    """_summary_

    Args:
        model_client (_type_): _description_
    """
    def classify(self, message: str) -> ClassificationResult:
        """_summary_

        Args:
            message (str): _description_

        Returns:
            ClassificationResult: _description_
        """
        return ClassificationResult(label="billing", confidence=0.94)

@pytest.mark.unit
def test_ticket_router_uses_classification_label():
    """Test that the TicketRouter uses the classification label from the model client."""
    router = TicketRouter(model_client=FakeModelClient())

    routed_ticket = router.route("I was charged twice.")

    assert routed_ticket.department == "billing"
    assert routed_ticket.confidence == 0.94

    
@pytest.mark.api
def test_create_ticket_returns_created_response(api_client):
    """Test that creating a ticket returns a 201 Created response."""
    response = api_client.post("/tickets", json={"message": "I was charged twice.   "}
                               )
    
    assert response.status_code == 201
    assert response.json() ["department"] == "billing"
