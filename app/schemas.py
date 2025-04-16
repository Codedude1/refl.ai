# app/schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict

class LogEntryOut(BaseModel):
    id: int
    message: str
    log_type: str
    quantity: Optional[float]
    unit: Optional[str]
    timestamp: datetime

    class Config:
        orm_mode = True

class SummaryOut(BaseModel):
    since: datetime
    total_entries: int
    counts_by_type: Dict[str, int]
