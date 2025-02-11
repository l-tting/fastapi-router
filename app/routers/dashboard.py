from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from auth import get_current_user
from database import get_db
import services

router = APIRouter()


@router.get('/sales_day')
def sales_per_day(user = Depends(get_current_user),db:Session =Depends(get_db)):
    sales_data  = services.sales_per_day(user,db)
    return {"Sales per day": sales_data}


@router.get('/sales_product')
def sales_per_product(user=Depends(get_current_user),db:Session = Depends(get_db)):
    sales_product = services.sales_per_product(user,db)
    return {"Sales per product":sales_product}


@router.get('/profit_day')
def profit_per_day(user=Depends(get_current_user),db:Session = Depends(get_db)):
    profit_day = services.profit_per_day(user,db)
    return {"Profit per day": profit_day}


@router.get('/profit_product')
def profit_per_product(user = Depends(get_current_user),db:Session = Depends(get_db)):
    profit_product = services.profit_per_product(user,db)
    return {"Profit per product":profit_product}


@router.get('/quick_stats')
def dashboard_quick_data(user=Depends(get_current_user),db:Session=Depends(get_db)):
    sales_today= services.get_sales_today(user,db)
    profit_today = services.get_profit_today(user,db)
    no_of_products=services.get_no_of_products(user,db)

    sales_this_month = services.get_sales_this_month(user,db)
    no_of_sales_today = services.get_saleno_today(user,db)
    monthly_profit = services.get_monthly_profit(user,db)
    low_stock_products = services.get_depleting_products(user,db)

    return {
        "sales_today":sales_today,
        "sales_this_month":sales_this_month,
        "no_of_sales_today":no_of_sales_today,
        "monthly_profit":monthly_profit,
        "no_of_products":no_of_products,
        "profit_today":profit_today,
        "low_stock":low_stock_products,
     }
