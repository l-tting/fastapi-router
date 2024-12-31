from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas
from database import get_db
from auth import get_current_user

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
def add_product(request: schemas.Product, user=Depends(get_current_user), db: Session = Depends(get_db)):
    new_product = models.Product(
        name=request.name,
        buying_price=request.buying_price,
        selling_price=request.selling_price,
        stock_quantity=request.stock_quantity
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {"message": "Product added successfully"}

@router.get("/", status_code=status.HTTP_200_OK)
def fetch_products(user=Depends(get_current_user), db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return {"products": products}

@router.get("/{product_id}", status_code=status.HTTP_200_OK)
def fetch_one_product(product_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", status_code=status.HTTP_200_OK)
def update_product(product_id: int, request: schemas.Product_Update, user=Depends(get_current_user), db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    # Update product fields
    if request.name: product.name = request.name
    if request.buying_price: product.buying_price = request.buying_price
    if request.selling_price: product.selling_price = request.selling_price
    if request.stock_quantity: product.stock_quantity = request.stock_quantity
    db.commit()
    db.refresh(product)
    return {"message": "Product updated successfully", "product": product}

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}
