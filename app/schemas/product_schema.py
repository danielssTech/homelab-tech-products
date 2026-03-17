from pydantic import BaseModel, ConfigDict

#Request
class ProductCreate(BaseModel):
    name: str
    price_cents: int

class ProductUpdate(BaseModel):
    name: str | None = None
    price_cents: int | None = None

#Response 
class ProductOut(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)

