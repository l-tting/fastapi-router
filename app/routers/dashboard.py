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
    sales_today= services.get_sales_today(user,db)
    profit_today = services.get_profit_today(user,db)
    no_of_products=services.get_no_of_products(user,db)
    sales_this_month = services.get_sales_this_month(user,db)
    no_of_sales_today = services.get_saleno_today(user,db)
    no_of_monthly_sales = services.get_no_of_monthly_sales(user,db)
    monthly_profit = services.get_monthly_profit(user,db)
    low_stock_number = services.get_depleting_products(user,db)
    lowest_stock_product = services.get_lowest_stock_product(user,db)
    highest_stock_product=services.get_highest_stock_product(user,db)

    stock_by_month = services.get_stock_by_month(user,db)
    first_five_sales= services.first_five_sales_product(user,db)
    sale_by_month = services.get_sale_by_month(user,db)
    profit_by_month = services.get_profit_by_month(user,db)
    stock_per_product = services.get_test_stock(user,db)
    return {
        "sales_today":sales_today,
        "sales_this_month":sales_this_month,
        "no_of_monthly_sales":no_of_monthly_sales,
        "no_of_sales_today":no_of_sales_today,
        "monthly_profit":monthly_profit,
        "no_of_products":no_of_products,
        "profit_today":profit_today,
        "low_stock":low_stock_number,
        "lowest_stock_product":lowest_stock_product,
        "highest_stock_product":highest_stock_product,
        "stock_by_month":stock_by_month,
        "first_five_sales":first_five_sales,
        "sale_by_month":sale_by_month,
        "profit_by_month":profit_by_month,
        "stock_per_product":stock_per_product,
     }


    