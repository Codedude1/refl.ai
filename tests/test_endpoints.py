import pytest
import sys
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app
from datetime import datetime, timedelta, timezone
from app.database import SessionLocal, engine
from app.models import Base, LogEntry

# Ensure the project root is on sys.path so `import app` works
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

@pytest.fixture(autouse=True)
def setup_db():
    # Recreate the database schema before each test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json() == {"message": "Reflect API is active!"}

def test_chat_and_logs_flow():
    # 1) Log an exercise entry with quantity/unit
    payload = {"message": "I ran 7 km today"}
    r1 = client.post("/chat", json=payload)
    assert r1.status_code == 200
    data = r1.json()["data"]
    assert data["log_type"] == "exercise"
    assert data["quantity"] == 7.0
    assert data["unit"] == "km"
    entry_id = data["id"]

    # 2) Retrieve it via /logs
    r2 = client.get("/logs?limit=1")
    assert r2.status_code == 200
    logs = r2.json()
    assert isinstance(logs, list) and len(logs) == 1

    log = logs[0]
    assert log["id"] == entry_id
    assert log["message"] == payload["message"]
    assert log["log_type"] == "exercise"
    assert log["quantity"] == 7.0
    assert log["unit"] == "km"
    assert "T" in log["timestamp"]

def test_weekly_summary_flow():
    # Seed two logs: one 10 days old, two recent
    now = datetime.now(timezone.utc)
    old = now - timedelta(days=10)

    db = SessionLocal()
    db.add_all([
        LogEntry(message="Old log",      log_type="general",  quantity=None,     unit=None, timestamp=old),
        LogEntry(message="Recent run",   log_type="exercise", quantity=5.0,      unit="km",   timestamp=now),
        LogEntry(message="Recent spend", log_type="expense",  quantity=100.0,    unit="₹",    timestamp=now),
    ])
    db.commit()
    db.close()

    r = client.get("/summary/weekly")
    assert r.status_code == 200
    data = r.json()
    assert data["total_entries"] == 2
    assert data["counts_by_type"] == {"exercise": 1, "expense": 1}
    assert "T" in data["since"]

def test_daily_summary_flow():
    # Seed one old (just over 24h ago) and one new (today)
    now = datetime.now(timezone.utc)
    just_over_24h = now - timedelta(days=1, seconds=1)

    db = SessionLocal()
    db.add_all([
        LogEntry(message="Old run",    log_type="exercise", quantity=3.0,  unit="km", timestamp=just_over_24h),
        LogEntry(message="Today spend",log_type="expense",  quantity=50.0, unit="$",  timestamp=now),
    ])
    db.commit()
    db.close()

    r = client.get("/summary/daily")
    assert r.status_code == 200
    data = r.json()
    # Only the "Today spend" should count
    assert data["total_entries"] == 1
    assert data["counts_by_type"] == {"expense": 1}
    assert "T" in data["since"]

def test_monthly_summary_flow():
    # Seed one old (31 days ago) and two within the last 30 days
    now = datetime.now(timezone.utc)
    old = now - timedelta(days=31)
    mid = now - timedelta(days=15)

    db = SessionLocal()
    db.add_all([
        LogEntry(message="Old log",       log_type="general",  quantity=None,   unit=None, timestamp=old),
        LogEntry(message="Mid‑month run", log_type="exercise", quantity=7.0,    unit="km",   timestamp=mid),
        LogEntry(message="Today spend",   log_type="expense",  quantity=200.0,  unit="₹",    timestamp=now),
    ])
    db.commit()
    db.close()

    r = client.get("/summary/monthly")
    assert r.status_code == 200
    data = r.json()
    assert data["total_entries"] == 2
    assert data["counts_by_type"] == {"exercise": 1, "expense": 1}
    assert "T" in data["since"]
