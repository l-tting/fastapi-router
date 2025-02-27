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
<<<<<<< Updated upstream
    db.add(new_stock)
=======
    
    db.add(new_stock_tracker)

    # Check if a stock record exists for this company and product
    existing_stock = db.query(models.Stock).filter_by(
        company_id=user.company_id, product_id=stock.product_id
    ).first()

    if existing_stock:
        # If stock exists, update the stock_count by adding the new stock to the existing one
        existing_stock.stock_count += stock.stock_count
    else:
        # If no stock exists for this product, create a new entry in the Stock table
        new_stock = models.Stock(
            company_id=user.company_id,
            product_id=stock.product_id,
            stock_count=stock.stock_count,
        )
        db.add(new_stock)

>>>>>>> Stashed changes
    db.commit()
    db.refresh(new_stock)
    return {"message": "Stock added successfully"}

<<<<<<< Updated upstream
@router.get("/depleted", status_code=status.HTTP_200_OK)
@admin_required
def depleted_stock(user=Depends(get_current_user), db: Session = Depends(get_db)):
    depleting_products = get_depleting_products(db)
    return {"depleting": depleting_products}
=======


@router.get('/',status_code=status.HTTP_200_OK)
def get_stock(user=Depends(get_current_user),db:Session=Depends(get_db)):
    my_stock = services.get_all_stock(user,db)
    if my_stock is None:
         raise HTTPException(status_code=404, detail="Stock not found")

    return {"my_stock":my_stock}


@router.get('/metrics',status_code=status.HTTP_200_OK)
def get_stock_data(user=Depends(get_current_user),db:Session=Depends(get_db)):
    stock_metrics = services.get_stock_metrics(user,db)
    stock_worth = services.get_stock_worth(user,db)
    return {"stock_metrics":stock_metrics,"stock_worth":stock_worth}
    

>>>>>>> Stashed changes
