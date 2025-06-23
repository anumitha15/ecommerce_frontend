from sqlalchemy import Column, Integer, String
from database import Base

class Product(Base):
    __tablename__ = "ProductImages"
    ProductID = Column(String, primary_key=True, index=True)
    ProductName = Column(String, index=True)
    Price = Column(Integer)
