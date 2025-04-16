# tests/test_nlp.py

from app.main import parse_message

def test_parse_exercise():
    log_type, qty, unit, _ = parse_message("I ran 5 km today")
    assert log_type == "exercise"
    assert qty == 5.0
    assert unit == "km"

def test_parse_expense():
    log_type, qty, unit, _ = parse_message("I spent 200 rs today on lunch")
    assert log_type == "expense"
    assert qty == 200.0
    # unit might be None or "rs" depending on your regex—adjust accordingly

def test_parse_general():
    log_type, qty, unit, _ = parse_message("Had a relaxed day!")
    assert log_type == "general"
    assert qty is None
    assert unit is None
