from sqlalchemy import Column, Integer, String, DateTime, func
from .db import Base

class AppProduct(Base):
    __tablename__ = "products"
    __table_args__ = {"schema": "app"}  

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price_cents = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

