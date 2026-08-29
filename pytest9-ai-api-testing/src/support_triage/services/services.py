from dataclasses import dataclass

@dataclass
class ClassificationResult:
    label: str
    confidence: float

@dataclass
class RoutedTicket:
    department: str
    confidence: float   

class TicketRouter:
    def __init__(self, model_client):
        self.model_client = model_client

    def route(self, message: str) -> RoutedTicket:
        result = self.model_client.classify(message)

        return RoutedTicket(
            department=classification_result.label,
            confidence=classification_result.confidence
        )   
