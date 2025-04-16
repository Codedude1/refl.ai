from sqlalchemy.orm import declarative_base
from sqlalchemy import (
    Column, Integer, String, DateTime, Float
)
import datetime

Base = declarative_base()

class LogEntry(Base):
    __tablename__ = "log_entries"
    id = Column(Integer, primary_key=True, index=True)
    message   = Column(String, nullable=False)
    log_type  = Column(String, nullable=False)   # e.g. "exercise", "expense", "cigarette", "water"
    quantity  = Column(Float,   nullable=True)   # e.g. 5.0
    unit      = Column(String,  nullable=True)   # e.g. "km", "cig", "L"
    value     = Column(String,  nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))

    def __repr__(self):
        return f"<LogEntry(id={self.id}, log_type='{self.log_type}', message='{self.message}')>"