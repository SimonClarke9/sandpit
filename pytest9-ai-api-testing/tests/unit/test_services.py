    """_summary_
    """

from dataclasses import dataclass

@dataclass
class ClassificationResult:
    """_summary_

    Args:
        labels (_type_): _description_
        confidence (_type_): _description_
    """
    labels: str
    confidence: float

@dataclass
class RoutedTicket:
    """_summary_

    Args:
        ticket_id (_type_): _description_
        classification (_type_): _description_
    """
    departmet: str
    confidence: float

class TicketRouter:
    """_summary_

    Args:
        model_client (_type_): _description_
    """
    def __init__(self, model_client):
        self.model_client = model_client

    def route(self, message : str) -> RoutedTicket:
        """_summary_

        Args:
            message (str): _description_

        Returns:
            RoutedTicket: _description_
        """
        result = self.model_client.classify(message)
        return RoutedTicket(
            departmet=result.labels,
            confidence=result.confidence
        )

      
    def route_ticket(self, ticket):
        """_summary_

        Args:
            ticket (_type_): _description_

        Returns:
            _type_: _description_
        """
        classification = self.model_client.classify(ticket["subject"])
        routed_ticket = RoutedTicket(
            departmet=classification.labels,
            confidence=classification.confidence
        )
        return routed_ticket