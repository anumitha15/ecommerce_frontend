from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine
from models import Product
import pyodbc
import schemas
from schemas import ProductCreate, ProductUpdate
from fastapi.middleware.cors import CORSMiddleware



# Create tables in database

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/products")
def read_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()

@app.post("/products")
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    new_product = models.Product(
        ProductName=product.ProductName,
        Price=product.Price
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@app.get("/products/{product_id}")
def get_product(product_id: str, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.ProductID == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
@app.put("/products/{product_id}")
def update_product(product_id: str, update_data: schemas.ProductUpdate, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.ProductID == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Update fields
    product.ProductName = update_data.ProductName
    product.Price = update_data.Price

    db.commit()
    db.refresh(product)
    return product

@app.delete("/products/{product_id}")
def delete_product(product_id: str):
    db = SessionLocal()
    try:
        product = db.query(Product).filter(Product.ProductID == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        db.delete(product)
        db.commit()
        return {"message": f"Product with ID '{product_id}' deleted successfully"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting product: {str(e)}")
    finally:
        db.close()