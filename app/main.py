from fastapi import FastAPI, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from datetime import datetime, timedelta, timezone

from app.models import Base, LogEntry
from app.database.database import engine, SessionLocal

from app.schemas import LogEntryOut, SummaryOut
from app.scheduler import start_scheduler

app = FastAPI(title="Reflect: AI-Powered Life Tracker")

@app.on_event("startup")
def _start_jobs():
        # 1) Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    # 2) Kick off your scheduler now you have a running loop
    start_scheduler()


class LogRequest(BaseModel):
    message: str


import re

def parse_message(msg: str):
    """
    Returns: (log_type, quantity, unit, free_text)
    """
    text = msg.lower()
    # Patterns: 5 km, 2.5l, 3 books, 4 cigs, 200 kcal, etc.
    m = re.search(r"(\d+(?:\.\d+)?)\s*(km|l|books?|cigs?|cigarettes?|kcal|\$|₹)?", text)
    qty, unit = (None, None)
    if m:
        qty  = float(m.group(1))
        unit = m.group(2) or None
    # Determine category
    if "run" in text or unit == "km":
        cat = "exercise"
    elif "cig" in text:
        cat = "cigarette"
    elif "water" in text or unit == "l":
        cat = "water"
    elif "spent" in text or "$" in text or "₹" in text:
        cat = "expense"
    elif "book" in text:
        cat = "book"
    else:
        cat = "general"
    return cat, qty, unit, msg


@app.post("/chat")
async def chat_endpoint(log: LogRequest):
    """
    Accept a chat message, parse it, save it, and return the entry ID and type.
    """
    cat, qty, unit, free_text = parse_message(log.message)
    new_log = LogEntry(
        message   = free_text,
        log_type  = cat,
        quantity  = qty,
        unit      = unit,
        value     = None,
        timestamp = datetime.now(timezone.utc),
    )

    db = SessionLocal()
    try:
        db.add(new_log)
        db.commit()
        db.refresh(new_log)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

    return {
        "status": "success",
        "data": {
            "id": new_log.id, 
            "log_type": cat,
            "quantity": new_log.quantity,
            "unit": new_log.unit
        }
    }


@app.get("/")
async def read_root():
    """
    Health check / root endpoint.
    """
    return {"message": "Reflect API is active!"}


@app.get("/logs", response_model=List[LogEntryOut])
async def get_logs(
    limit: int = Query(10, description="Number of log entries to retrieve")
):
    """
    Return the most recent `limit` log entries.
    """
    db: Session = SessionLocal()
    try:
        entries = (
            db.query(LogEntry)
              .order_by(LogEntry.timestamp.desc())
              .limit(limit)
              .all()
        )
        return [
            {
                "id": e.id,
                "message": e.message,
                "log_type": e.log_type,
                "quantity": e.quantity,
                "unit": e.unit,
                "timestamp": e.timestamp.isoformat(),
            }
            for e in entries
        ]
    finally:
        db.close()


def get_db():
    """
    Dependency to get a DB session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/summary/weekly", response_model=SummaryOut)
def weekly_summary(db: Session = Depends(get_db)):
    """
    Summarize how many entries of each type have been logged
    in the last 7 days.
    """
    cutoff = datetime.now(timezone.utc) - timedelta(days=7)
    entries = (
        db.query(LogEntry)
          .filter(LogEntry.timestamp >= cutoff)
          .all()
    )

    counts: dict[str, int] = {}
    for e in entries:
        counts[e.log_type] = counts.get(e.log_type, 0) + 1

    return {
        "since": cutoff.isoformat(),
        "total_entries": len(entries),
        "counts_by_type": counts,
    }

@app.get("/summary/daily", response_model=SummaryOut)
def daily_summary(db: Session = Depends(get_db)):
    """
    Summarize how many entries of each type have been logged
    in one day.
    """
    cutoff = datetime.now(timezone.utc) - timedelta(days=1)
    entries = (
        db.query(LogEntry)
          .filter(LogEntry.timestamp >= cutoff)
          .all()
    )

    counts: dict[str, int] = {}
    for e in entries:
        counts[e.log_type] = counts.get(e.log_type, 0) + 1

    return {
        "since": cutoff.isoformat(),
        "total_entries": len(entries),
        "counts_by_type": counts,
    }

@app.get("/summary/monthly", response_model=SummaryOut)
def monthly_summary(db: Session = Depends(get_db)):
    """
    Summarize how many entries of each type have been logged
    in a month.
    """
    cutoff = datetime.now(timezone.utc) - timedelta(days=30)
    entries = (
        db.query(LogEntry)
          .filter(LogEntry.timestamp >= cutoff)
          .all()
    )

    counts: dict[str, int] = {}
    for e in entries:
        counts[e.log_type] = counts.get(e.log_type, 0) + 1

    return {
        "since": cutoff.isoformat(),
        "total_entries": len(entries),
        "counts_by_type": counts,
    }
