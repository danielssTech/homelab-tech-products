import time
from fastapi import FastAPI, Depends, Path, status, HTTPException, Request
from app.core.logging import setup_logging
from app.routes import appProducts, health
from . import models
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from contextlib import asynccontextmanager
from .db import engine, SessionLocal
from starlette.responses import Response
from fastapi.responses import JSONResponse
from sqlalchemy.exc import OperationalError, IntegrityError, SQLAlchemyError
from prometheus_fastapi_instrumentator import Instrumentator

logger = setup_logging()
app = FastAPI() 

# --- Instrumentator global ---
instrumentator = Instrumentator().instrument(app)
instrumentator.expose(app, endpoint="/metrics", include_in_schema=False)


models.Base.metadata.create_all(bind=engine)

app.include_router(appProducts.product_router)
app.include_router(health.helth_router)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    try:
        response: Response = await call_next(request)
        return response
    finally:
        duration_ms = (time.perf_counter() - start) * 1000
        logger.info(
            "%s %s -> %s (%.2f ms)",
            request.method,
            request.url.path,
            getattr(response, "status_code", "NA"),
            duration_ms,
        )

# 503 si la DB no responde, timeout, DNS, etc.
@app.exception_handler(OperationalError)
async def op_error_handler(request: Request, exc: OperationalError):
    logger.error("DB OperationalError on %s %s :: %s", request.method, request.url.path, str(exc))
    return JSONResponse(
        status_code=503,
        content={"detail": "Database unavailable. Please try again later."},
    )

# 409 si violas constraints (únicos, FK, etc.)
@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    logger.warning("IntegrityError on %s %s :: %s", request.method, request.url.path, str(exc))
    return JSONResponse(
        status_code=409,
        content={"detail": "Integrity error: constraint violation."},
    )

# Cualquier otro error de SQLAlchemy
@app.exception_handler(SQLAlchemyError)
async def sa_error_handler(request: Request, exc: SQLAlchemyError):
    logger.error("SQLAlchemyError on %s %s :: %s", request.method, request.url.path, str(exc))
    return JSONResponse(
        status_code=500,
        content={"detail": "Database error."},
    )

# Fallback genérico
@app.exception_handler(Exception)
async def unhandled_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error on %s %s :: %s", request.method, request.url.path, str(exc))
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error."},
    )

