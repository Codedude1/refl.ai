
from app.database import engine, SessionLocal
from app.models import Base

def init_db(drop: bool = True):
    if drop:
        Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized. Tables:", Base.metadata.tables.keys())

if __name__ == "__main__":
    init_db()
