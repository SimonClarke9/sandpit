"""  Module for calculator functions"""

from support_triage.calculator import add

def test_add():
    """_summary_
    """
    assert add(1, 2) == 3
    assert add(-1, 1) == 0
    assert add(0, 0) == 0

def test_add_returns_sum():
    """Test that add() returns the correct sum."""
    result = add(2, 3)
    assert result == 5
# End-of-file (EOF)