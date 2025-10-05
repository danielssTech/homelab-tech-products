from fastapi import APIRouter, status
from sqlalchemy import text
from app.db import engine

helth_router = APIRouter(prefix="/api", tags=["health"])

@helth_router.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"status": "ok", "db": "up"}