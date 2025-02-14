from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from models import Sale,Product,User,Company,Stock
from sqlalchemy.ext.asyncio import AsyncSession
from auth import get_current_user



def sales_per_day(user:get_current_user,db:Session):
    sales_day_day= db.query(func.date(Sale.created_at).label("dates"),
                    func.sum(Sale.quantity * Product.selling_price).label("sales")).join(Product).filter(user.company_id==Company.id).group_by('dates').all()
  
    sales_data =[{"date":str(dates),"sales":sales} for dates,sales in sales_day_day]

    return sales_data



def sales_per_product(user:get_current_user,db:Session):
    sales_per_prod = db.query((Product.name).label("product"),
                        func.sum(Product.selling_price * Sale.quantity).label("sales")).join(Sale).join(Company).filter(user.company_id==Company.id).group_by("product").all()
    sales_prod =[{"product":product,"sale":sale} for product,sale in sales_per_prod]
    return sales_prod


def profit_per_day(user:get_current_user,db:Session):
    profit_day = db.query(func.date(Sale.created_at).label("dates"),
                          func.sum(Sale.quantity*(Product.selling_price -Product.buying_price)).label("profit")).join(Product).filter(user.company_id==Company.id).group_by('dates').all()
    profit_data =[{"date":dates,"profit":profit} for dates,profit in profit_day]
    return profit_data


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
    products = db.query(Product).join(Company).filter(user.company_id==Company.id).all()
    return len(products)


def get_no_of_users(user:get_current_user,db:Session):
    users = db.query(User).join(Company,Company.id==User.company_id).filter(user.company_id==Company.id).all()
    return len(users)


def get_saleno_today(user:get_current_user,db:Session):
    no_of_sales_today = db.query(Sale).join(Company,Company.id==Sale.company_id).filter(user.company_id==Company.id).filter(func.date(Sale.created_at) == date.today()).all()
    return len(no_of_sales_today)


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


def get_sales_this_month(user: get_current_user, db: Session):
    sales_this_month = db.query(func.sum(Sale.quantity * Product.selling_price).label('total_sales')
    ).select_from(Sale)\
     .join(Product, Sale.pid == Product.id)\
     .join(Company, Product.company_id == Company.id)\
     .filter(func.extract('year', Sale.created_at) == date.today().year) \
     .filter(func.extract('month', Sale.created_at) == date.today().month) \
     .filter(Company.id == user.company_id).scalar()
    return sales_this_month

def get_no_of_monthly_sales(user:get_current_user,db:Session):
    no_of_sales = db.query(Sale).filter(Sale.company_id==user.company_id).all()
    if no_of_sales:
        return len(no_of_sales)
    return None


def get_profit_today(user:get_current_user,db:Session):
    profit_today = db.query(func.sum((Sale.quantity*(Product.selling_price - Product.buying_price)))).join(Product).join(Company).filter(func.date(Sale.created_at)==date.today(),user.company_id==Company.id).group_by(Company.company_name).scalar()
    return profit_today if profit_today is not None else 0


def get_monthly_profit(user:get_current_user,db:Session):
    monthly_profit = db.query(func.sum((Sale.quantity*(Product.selling_price - Product.buying_price)))).join(Product).join(Company)\
                .filter(func.extract('year', Sale.created_at) == date.today().year) \
                .filter(func.extract('month', Sale.created_at) == date.today().month) \
                .filter(Company.id == user.company_id).scalar()
    return monthly_profit


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



def get_sale_by_month(user, db: Session):
    sale_by_month = (
        db.query(
            func.date_trunc('month', Sale.created_at).label('month'),  

            func.sum(Sale.quantity * Product.selling_price).label('total_sales'))
        .join(Product, Sale.pid == Product.id)  
        .filter(Sale.company_id == user.company_id)  
        .group_by(func.date_trunc('month', Sale.created_at), Product.id)  
        .all()  
    )
    if sale_by_month:
        formatted_sale_by_month = [{"month": month.strftime('%m'),  "total_sales": total_sales}
            for month,  total_sales in sale_by_month]
        return formatted_sale_by_month
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
