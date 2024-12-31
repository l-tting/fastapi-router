from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas
from database import get_db
from auth import get_current_user
from utils import admin_required
from services import get_depleting_products

router = APIRouter()

@router.post("/add", status_code=status.HTTP_201_CREATED)
@admin_required
def add_stock(stock: schemas.Stock, user=Depends(get_current_user), db: Session = Depends(get_db)):
    new_stock = models.Stock(
        product_name=stock.product_name,
        stock_count=stock.stock_count,
        vendor_name=stock.vendor_name
    )
    db.add(new_stock)
    db.commit()
    db.refresh(new_stock)
    return {"message": "Stock added successfully"}

@router.get("/depleted", status_code=status.HTTP_200_OK)
@admin_required
def depleted_stock(user=Depends(get_current_user), db: Session = Depends(get_db)):
    depleting_products = get_depleting_products(db)
    return {"depleting": depleting_products}
