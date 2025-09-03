from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.settings import settings

engine = create_engine (
    settings.db_url, 
    pool_pre_ping=True, 

)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# Dep para FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()