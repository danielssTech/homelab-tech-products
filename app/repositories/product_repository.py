#DB access 
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import select, delete, update
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

def get_product_repository (db: Session, id: int):
    
    stmt = select(product.AppProduct).where(product.AppProduct.id == id )
    result = db.execute(stmt).scalar_one_or_none()
    return result

def delete_product_repository(db: Session, id: int) -> int:
    stmt = delete(product.AppProduct).where(product.AppProduct.id == id)
    result = db.execute(stmt)
    db.commit()
    return result.rowcount

def update_product_repository(db: Session, id: int, request: product_schema.ProductUpdate) -> int:
    stmt = update(product.AppProduct).where(product.AppProduct.id == id).values(name = request.name)
    result = db.execute(stmt)
    db.commit()
    return result.rowcount