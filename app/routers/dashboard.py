from fastapi import APIRouter,Depends,Request
from sqlalchemy.orm import Session
from limiter import limiter
from auth import get_current_user
from database import get_db
import services

router = APIRouter()

@router.get('/sales_day')
@limiter.limit("30/minute")
def sales_per_day(request: Request,user = Depends(get_current_user),db:Session =Depends(get_db)):
    sales_data  = services.sales_per_day(user,db)
    return {"sales_per_day": sales_data}


@router.get('/sales_product')
@limiter.limit("30/minute")
def sales_per_product(request: Request,user=Depends(get_current_user),db:Session = Depends(get_db)):
    sales_product = services.sales_per_product(user,db)
    return {"sales_per_product":sales_product}

@router.get('/profit_data')
def profit_time(user=Depends(get_current_user),db:Session = Depends(get_db)):
    profit_data = services.get_profit_time_data(user,db)
    return {"prof_data":profit_data}


@router.get('/profit_day')
@limiter.limit("30/minute")
def profit_per_day(request: Request,user=Depends(get_current_user),db:Session = Depends(get_db)):
    profit_day = services.profit_per_day(user,db)
    return {"profit_per_day": profit_day}


@router.get('/profit_product')
@limiter.limit("30/minute")
def profit_per_product(request: Request,user = Depends(get_current_user),db:Session = Depends(get_db)):
    profit_product = services.profit_per_product(user,db)
    return {"profit_per_product":profit_product}


@router.get('/quick_stats')
@limiter.limit("30/minute")
async def dashboard_quick_data(request: Request,user=Depends(get_current_user),db:Session=Depends(get_db)):
    
    low_stock_number = services.get_depleting_products(user,db)
    stock_by_month = services.get_stock_by_month(user,db)
    first_five_sales= services.first_five_sales_product(user,db)
    profit_by_month = services.get_profit_by_month(user,db)
    stock_per_product = services.get_test_stock(user,db)
    return {
        
        "low_stock":low_stock_number,
        "stock_by_month":stock_by_month,
        "first_five_sales":first_five_sales,
        "profit_by_month":profit_by_month,
        "stock_per_product":stock_per_product,
     }


    