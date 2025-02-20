from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas,services
from database import get_db
from auth import get_current_user
from utils import admin_required
from services import get_depleting_products

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
def add_stock(stock: schemas.Stock, user=Depends(get_current_user), db: Session = Depends(get_db)):
    new_stock = models.Stock(
        company_id = user.company_id,
        product_id=stock.product_id,
        stock_count=stock.stock_count,
    )
    check_product = db.query(models.Product).filter(models.Product.id==stock.product_id,models.Product.company_id==user.company_id).first()
    print(check_product.name)
    if not check_product:
        raise HTTPException(status_code=404,detail=f'Product with product id:{stock.product_id} not found')
    db.add(new_stock)
    db.commit()
    db.refresh(new_stock)
    return {"message": "Stock added successfully"}


@router.get('/',status_code=status.HTTP_200_OK)
def get_stock(user=Depends(get_current_user),db:Session=Depends(get_db)):
    my_stock = db.query(models.Stock).filter(models.Stock.company_id==user.company_id).all()
    if my_stock is None:
         raise HTTPException(status_code=404, detail="Stock not found")
    
    stock_data =[]
    for stock in my_stock:
        formatted_created_at = stock.created_at.strftime("%H:%M: -> %d- %B -%Y")
        stock_data.append({
            "id":stock.id,
            "cid":stock.company_id,
            "product_id":stock.product_id,
            "stock_count":stock.stock_count,
            "created_at":formatted_created_at,
        })

    return {"my_stock":stock_data}

@router.get('/metrics',status_code=status.HTTP_200_OK)
def get_stock_data(user=Depends(get_current_user),db:Session=Depends(get_db)):
    stock_metrics = services.get_stock_metrics(user,db)
    stock_worth = services.get_stock_worth(user,db)
    return {"stock_metrics":stock_metrics,"stock_worth":stock_worth}
    

