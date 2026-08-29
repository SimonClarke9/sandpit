"""_summary_"""


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
        return ClassificationResult(labels="billing", confidence=0.94)



    @pytest.mark.unit
    def test_ticket_router_uses_classification_label(self): 
        """_summary_
        """
        router= TicketRouter( model_client=FakeModelClient()   )

        routed_ticket = router.route("I was charged twice.")

        assert routed_ticket.department == "billing"
        assert routed_ticket.confidence == 0.94 
        