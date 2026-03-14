from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.core.db import get_db
from app.schemas import product_schema
from sqlalchemy.exc import IntegrityError

from app.models import product


product_router = APIRouter (tags=["techProduct"])

@product_router.post('/products', status_code=status.HTTP_201_CREATED)
def create (request: product_schema.ProductCreate, db: Session = Depends(get_db) ): 
    new_product =  product.AppProduct (
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


@product_router.get('/products_get', response_model=list[product_schema.ProductOut])
def list_items(skip: int = Query(0, ge=0),limit: int = Query(10, ge=1, le=100),
               db: Session = Depends(get_db),):
    stmt = select(product.AppProduct).offset(skip).limit(limit)
    rows = db.execute(stmt).scalars().all()
    return rows


