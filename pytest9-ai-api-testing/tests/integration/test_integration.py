import pytest

@pytest.mark.integration
@pytest.mark.requires_docker


def test_ticket_repository_saves_ticket(ticket_repository):
    ticket = ticket_repository.create(message="I was charged twice.")

    saved_ticket = ticket_repository.get(ticket.id) 

    assert saved_ticket.message == "I was charged twice."

