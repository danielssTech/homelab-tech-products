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