from fastapi import FastAPI, Depends, Path, status, HTTPException

from . import models #verificar si es que esta bien importado 

from sqlalchemy.orm import Session
from passlib.context import CryptContext
from contextlib import asynccontextmanager


app = FastAPI() 

@app.get("/health")
def health_check():
    return {"status": "ok"}