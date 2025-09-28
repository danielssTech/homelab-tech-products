from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db import get_db
from app import models, schemas
from sqlalchemy.exc import IntegrityError


product_router = APIRouter (tags=["techProduct"])

@product_router.post('/products', status_code=status.HTTP_201_CREATED)
def create (request: schemas.ProductCreate, db: Session = Depends(get_db) ): 
    new_product =  models.AppProduct (
        name= request.name, 
        price_cents=request.price_cents 
    )
    db.add (new_product)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise e
    except Exception:
        db.rollback()
        raise
    db.refresh(new_product)
    return new_product


@product_router.get('/products_get', response_model=list[schemas.ProductOut])
def list_items(skip: int = Query(0, ge=0),limit: int = Query(10, ge=1, le=100),
               db: Session = Depends(get_db),):
    stmt = select(models.AppProduct).offset(skip).limit(limit)
    rows = db.execute(stmt).scalars().all()
    return rows


