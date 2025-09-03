from fastapi import FastAPI, Depends, Path, status, HTTPException
from app.routes import appProducts, health
from . import models
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from contextlib import asynccontextmanager
from .db import engine, SessionLocal

app = FastAPI() 

models.Base.metadata.create_all(bind=engine)

app.include_router(appProducts.product_router)
app.include_router(health.helth_router)


