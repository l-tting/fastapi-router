from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date,datetime
from models import Sale,Product,User,Company,Stock
from sqlalchemy.ext.asyncio import AsyncSession
from auth import get_current_user
from fastapi import HTTPException



def sales_per_day(user:get_current_user,db:Session):
    try:
        sales_per_day= db.query(func.date(Sale.created_at).label("dates"),
                        func.sum(Sale.quantity * Product.selling_price).label("sales")).join(Product,Product.id==Sale.pid).join(Company,Company.id==Sale.company_id
                        ).filter(user.company_id==Company.id).group_by('dates')
        sale_today = sales_per_day.filter(func.date(Sale.created_at)==date.today()).all()
        all_sales_per_day = sales_per_day.group_by('dates').all()
        if sales_per_day:
            sales_data_today =[{"date":str(dates),"sales":sales} for dates,sales in sale_today]
            sales_data_all =[{"date":str(dates),"sales":sales} for dates,sales in all_sales_per_day]
            return {"sales_today":sales_data_today if sales_data_today else 0,"all_sale_data":sales_data_all}
        raise HTTPException(status_code=404,detail='Sales per day no found')
    except Exception as error:
        raise HTTPException(status_code=500,detail={"Error fetching sales per day":error})


def get_sale_time_data(user, db: Session):
    # Fetch sales data grouped by month
    sale_per_timedelta =  db.query(
            func.date( Sale.created_at).label('dates'),
            func.sum(Sale.quantity * Product.selling_price).label('total_sales')
        ).join(Product, Sale.pid == Product.id).filter(Sale.company_id == user.company_id).group_by(Sale.created_at).all()
    

  
    formatted_sale_per_timedelta = [{"date":dates,"sales":sale} for dates, sale in sale_per_timedelta] if sale_per_timedelta else 0
    return formatted_sale_per_timedelta

def sales_per_product(user:get_current_user,db:Session):
    try:
        sales_per_prod = db.query((Product.name).label("product"),
                            func.sum(Product.selling_price * Sale.quantity).label("sales")).join(Sale).join(Company).filter(user.company_id==Company.id).group_by("product").all()
        if sales_per_prod:
            sales_prod =[{"product":product,"sale":sale} for product,sale in sales_per_prod]
            return sales_prod
        raise HTTPException(status_code=404,detail=f'{error}')
    except Exception as error:
        raise HTTPException(status_code=500,detail=f'{error}')


def profit_per_day(user:get_current_user,db:Session):
    try:
        profit_day = db.query(func.date(Sale.created_at).label("dates"),
                            func.sum(Sale.quantity*(Product.selling_price -Product.buying_price)).label("profit")).join(Product).filter(user.company_id==Company.id).group_by('dates').all()
        if profit_day:
            profit_data =[{"date":dates,"profit":profit} for dates,profit in profit_day]
            return profit_data
        raise HTTPException(status_code=404,detail='Profit per day data not found')
    except Exception as error:
        raise HTTPException(status_code=500,detail=f'{error}')


def profit_per_product(user: get_current_user, db: Session):
    profit_product = db.query(
        Product.name.label("product"),
        func.sum(Sale.quantity * (Product.selling_price - Product.buying_price)).label("profit")
    ).join(Sale).join(Company).filter(Company.id == user.company_id).group_by(Product.name).order_by(
        func.sum(Sale.quantity * (Product.selling_price - Product.buying_price)).desc())
    if profit_product:
        profit_p = [{"product": product, "profit": profit} for product, profit in profit_product.all()]
        profit_five = [{"product": product, "profit": profit} for product, profit in profit_product.limit(5)]
        return {"profit_all_prods": profit_p, "profit_five_prods": profit_five}
    
    return None


def get_no_of_products(user:get_current_user,db:Session):
    try:
        products = db.query(Product).join(Company).filter(user.company_id==Company.id).all()
        return len(products) if products else 0
    except Exception as e:
        raise HTTPException(status_code=500,detail={"Error fetching no of prods":e})


def get_no_of_users(user:get_current_user,db:Session):
    try:
        users = db.query(User).join(Company,Company.id==User.company_id).filter(user.company_id==Company.id).all()
        return len(users) if users else 0
    except Exception as e:
        raise HTTPException(status_code=500,detail={"Error fetching no of users":e})


# def get_saleno_today(user:get_current_user,db:Session):
#     no_of_sales_today = db.query(Sale).join(Company,Company.id==Sale.company_id).filter(user.company_id==Company.id).filter(func.date(Sale.created_at) == date.today()).all()
#     return len(no_of_sales_today)


def get_sales_today(user: get_current_user, db: Session):
    sales_today = db.query(
        func.sum(Sale.quantity * Product.selling_price).label('total_sales')
    ).select_from(Sale) \
    .join(Product, Sale.pid == Product.id) \
    .join(Company, Product.company_id == Company.id) \
    .filter(func.date(Sale.created_at) == date.today()) \
    .filter(Company.id == user.company_id) \
    .scalar()  
    return sales_today if sales_today is not None else 0



def get_no_of_monthly_sales(user:get_current_user,db:Session):
    no_of_sales = db.query(Sale).filter(Sale.company_id==user.company_id).all()
    if no_of_sales:
        return len(no_of_sales)
    return None





def get_depleting_products(user:get_current_user,db:Session):
    products = db.query(Stock).filter(Stock.stock_count < 20).filter(Stock.company_id==user.company_id).all()
    # data = [lowstock for lowstock in products]
    print(f"Test {products}")
    return len(products)


def get_products_by_company(user:get_current_user,db:Session):
    products = db.query(Product).join(Company,Company.id==Product.company_id).filter(Company.id==user.company_id).all()
    company_pids = {p.id for p in products}
    return company_pids

def get_total_users(user:get_current_user,db:Session):
    users = db.query(User).join()

def get_lowest_stock_product(user:get_current_user,db:Session):
    lowest_stock_product = db.query(Product.name,Stock.stock_count).join(Product,Product.id==Stock.product_id).filter(Stock.company_id==user.company_id).order_by(Stock.stock_count.asc()).first()
    if lowest_stock_product:
        return {
            "product_name": lowest_stock_product[0],  # Product name
            "stock_count": lowest_stock_product[1]    # Stock count
        }
    return None

def get_highest_stock_product(user,db:Session):
    highest_stock_product = db.query(Product.name,Stock.stock_count).join(Product,Product.id==Stock.product_id).filter(Stock.company_id==user.company_id).order_by(Stock.stock_count.desc()).first()
    if highest_stock_product:
        return {
            "product_name": highest_stock_product[0],  # Product name
            "stock_count": highest_stock_product[1]    # Stock count
        }
    return None

def get_highest_lowest_stock(user,db):
    try:
        high_low_stock = db.query(Product.name,Stock.stock_count).join(Product,Product.id==Stock.product_id).filter(Stock.company_id==user.company_id)
        
        highest_stock_prod = high_low_stock.order_by(Stock.stock_count.desc()).first()
        lowest_stock_prod = high_low_stock.order_by(Stock.stock_count.asc()).first()
        return {
            "highest_stock_product":{ 
             "product_name": highest_stock_prod[0],  
            "stock_count": highest_stock_prod[1] 
            },
            "lowest_stock_prod":{
                "product_name": lowest_stock_prod[0],  
                "stock_count": lowest_stock_prod[1]    
            }
            }
    except Exception as e:
        raise HTTPException(status_code=500,detail={"Error fetching highe and low stock":e})


def get_first_five_stock(user,db:Session):
    first_five = db.query(Product.name,Stock.stock_count).join(Product,Product.id==Stock.product_id).filter(Product.company_id==user.company_id).order_by(Stock.stock_count.desc()).limit(5)
    if first_five:
        result = [{"product_name": name, "stock_count": stock_count} for name, stock_count in first_five.all()]
        return result
    return None


def get_stock_by_month(user,db:Session):
    stock_by_month = db.query(func.date_trunc('month', Stock.created_at).label('month'),
        func.sum(Stock.stock_count).label('total_stock')
        ).filter(Stock.company_id==user.company_id).group_by('month').order_by('month').all()
    print(stock_by_month)
    if stock_by_month:
        formatted_stock_by_month = [{"month": month.strftime('%m'), "total_stock": total_stock} for month, total_stock in stock_by_month]
        return formatted_stock_by_month
    return None



def get_profit_by_month(user,db:Session):
    profit_by_month = db.query( func.date_trunc('month', Sale.created_at).label('month'), 
                        func.sum(Sale.quantity * (Product.selling_price-Product.buying_price).label('total_profit'))
                    ).join(Product, Sale.pid == Product.id).filter(Sale.company_id == user.company_id).group_by(func.date_trunc('month', Sale.created_at), Product.id).all()  

    if profit_by_month:
        formattted_profit_by_month = [{"month": month.strftime('%m'),"total_profit":total_profit} for month,total_profit in profit_by_month]
        return formattted_profit_by_month
    return None
                        
    
def first_five_sales_product(user,db:Session):
    five_sales_product = db.query(Product.name,(Sale.quantity * (Product.selling_price)).label('sales')).join(
        Sale,Sale.pid==Product.id).filter(Product.company_id==user.company_id).order_by(Sale.quantity * Product.selling_price).limit(5).all()
    if five_sales_product:
        formatted_five_sales_product =[{"product_name":name,"stock_count":stock_count} for name,stock_count in five_sales_product]
        return formatted_five_sales_product
    return None


def get_stock_per_product(user,db:Session):
    stock_per_product = db.query(Product.name,Stock.stock_count).join(Stock,Stock.product_id==Product.id
            ).filter(Company.id==user.company_id).all()
    if stock_per_product:
        formatted_stock_per_product = [{"product_name":name,"stock_count":stock_count} for name,stock_count in stock_per_product]
        return formatted_stock_per_product
    return None


def get_test_stock(user,db:Session):
    test_stock = db.query(Product.name,Stock.stock_count).join(Product,Product.id==Stock.product_id).filter(Product.company_id==user.company_id).order_by(Stock.stock_count.desc())
    first_five = test_stock.limit(5).all()
    all_stock = test_stock.all()
    if test_stock:
        result_five = [{"product_name":name,"stock_count":stock_count} for name ,stock_count in first_five]
        rest_stock = [{"product_name":name,"stock_count":stock_count} for name,stock_count in all_stock]
        return {
            "five":result_five,
            "all":rest_stock,
        }
    return None


def get_profit_time_data(user, db: Session):
    # Calculate the markup for profit
    markup = Product.selling_price - Product.buying_price

    # Fetch all profit data grouped by date (this already sums profits)
    all_profit = db.query(func.date(Sale.created_at).label('dates'),func.sum(Sale.quantity * markup).label("profit")
    ).join(Product, Product.id == Sale.pid) \
    .filter(Sale.company_id == user.company_id).group_by(func.date(Sale.created_at)).all()

    # Format the profit data for each date
    formatted_profit = [{"date": dates, "profit": profit} for dates, profit in all_profit] if all_profit else []

    today_date = date.today()
    today_profit = next((item['profit'] for item in formatted_profit if item['date'] == today_date), None)  

    current_month = date.today().month
    current_year = date.today().year
    monthly_profit = sum(
        item['profit'] for item in formatted_profit if item['date'].year == current_year and item['date'].month == current_month )

    return {"formatted":formatted_profit,"today":today_profit,"month":monthly_profit}  
  

