from pydantic import BaseModel

class ProductCreate(BaseModel):
    ProductName: str
    Price: int
class ProductUpdate(BaseModel):
    ProductName: str
    Price: int