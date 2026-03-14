#DB access 
#business logic
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import product
from app.schemas import product_schema
from sqlalchemy.exc import IntegrityError


def get_products_repository (skip: int, limit: int, db: Session):
    stmt = select(product.AppProduct).offset(skip).limit(limit)
    rows = db.execute(stmt).scalars().all()
    return rows

def post_product_service (request: product_schema.ProductCreate, db: Session): 
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