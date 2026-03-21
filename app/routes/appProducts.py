from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.core.db import get_db
from app.schemas import product_schema
from sqlalchemy.exc import IntegrityError

from app.models import product
from app.services import product_service

product_router = APIRouter (tags=["techProduct"])


@product_router.get('/products_get', response_model=list[product_schema.ProductOut])
def list_items(skip: int = Query(0, ge=0),limit: int = Query(10, ge=1, le=100),
               db: Session = Depends(get_db)):
    return product_service.get_products_service(skip=skip, limit=limit, db=db)

@product_router.get('/product/{id}', response_model=product_schema.ProductOut)
def get_item(  id: int , db: Session = Depends(get_db)):
    return product_service.get_product_service(db, id)

@product_router.post('/products', status_code=status.HTTP_201_CREATED)
def create (request: product_schema.ProductCreate, db: Session = Depends(get_db) ): 
    return product_service.post_product_service(request, db)

@product_router.delete('/product/{id}')
def delete_item (id: int, db: Session = Depends(get_db)):
    return product_service.delete_product_service(db, id)

@product_router.put('/product/{id}')
def update_item (request: product_schema.ProductUpdate, id: int , db: Session = Depends(get_db)):
    return product_service.update_product_service(db,id,request)
