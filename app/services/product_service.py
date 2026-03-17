#business logic
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import product
from app.repositories import product_repository
from app.schemas import product_schema

def get_products_service (skip: int, limit: int, db: Session):
    return product_repository.get_products_repository(skip=skip,limit=limit,db=db)

def post_product_service (request: product_schema.ProductCreate, db: Session): 
    return product_repository.post_product_service(request, db)


def get_product_service(db: Session, id: int):
    product_obj = product_repository.get_product_repository(db, id)

    if product_obj is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return product_obj

def delete_product_service(db: Session, id: int):
    deleted_rows = product_repository.delete_product_repository(db, id)

    if deleted_rows == 0:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"message": "Product deleted successfully"}

def update_product_service (db: Session, id: int, request: product_schema.ProductUpdate):
    update_rows = product_repository.update_product_repository(db, id, request)

    if update_rows == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return {"message": "Product updated successfully"}
