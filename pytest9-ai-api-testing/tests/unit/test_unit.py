"""  Unit Test script
"""

import pytest

@pytest.mark.unit
def test_ticket_priority_defualts_to_normal():
    ticket = {"subject" : "Question about billing"}

    priority = "npormal" if "urgent" not in ticket["subject"].lower() else "high"

    assert priority == "normal"
