from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from models import Sale,Product,User,Company
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

def profit_per_product(user:get_current_user,db:Session):
    profit_product = db.query((Product.name).label("product"),
            func.sum(Sale.quantity *(Product.selling_price-Product.buying_price)).label("Profit")).join(Sale).join(Company).filter(Company.id==user.company_id).group_by("product").all()
    
    profit_p =[{"product":product,"profit":profit} for product,profit in profit_product]
    return profit_p

def get_no_of_products(user:get_current_user,db:Session):
    products = db.query(Product).filter(user.company_id==Company.id).all()
    return len(products)

def get_no_of_users(user:get_current_user,db:Session):
    users = db.query(User).join(Company,Company.id==User.company_id).filter(user.company_id==Company.id).all()
    return len(users)

def get_saleno_today(user:get_current_user,db:Session):
    no_of_sales_today = db.query(Sale).join(Company,Company.id==Sale.company_id).filter(user.company_id==Company.id).all()
    return len(no_of_sales_today)

def get_sales_today(user:get_current_user,db:Session):
    sales_today = db.query(
    Company.company_name,
    func.sum(Sale.quantity * Product.selling_price).label('total_sales')
    ).select_from(Sale)\
    .join(Product, Sale.pid == Product.id).join(Company, Product.company_id == Company.id).filter(func.date(Sale.created_at) == date.today()).filter(Company.id == user.company_id).group_by(Company.company_name) 

    return sales_today

from sqlalchemy import func
from datetime import date

def get_sales_this_month(user: get_current_user, db: Session):
    sales_this_month = db.query(
        Company.company_name,
        func.sum(Sale.quantity * Product.selling_price).label('total_sales')
    ).select_from(Sale)\
     .join(Product, Sale.pid == Product.id)\
     .join(Company, Product.company_id == Company.id)\
     .filter(func.extract('year', Sale.created_at) == date.today().year) \
     .filter(func.extract('month', Sale.created_at) == date.today().month) \
     .filter(Company.id == user.company_id)\
     .group_by(Company.company_name)

    return sales_this_month



def get_profit_today(user:get_current_user,db:Session):
    profit_today = db.query(func.sum((Sale.quantity*(Product.selling_price - Product.buying_price)))).join(Product).join(Company).filter(func.date(Sale.created_at)==date.today(),user.company_id==Company.id).group_by(Company.company_name).scalar()
    return profit_today

def get_depleting_products(user:get_current_user,db:Session):
    products = db.query(Product).filter(Product.stock_quantity < 20).all()
    # data = [lowstock for lowstock in products]
    return products

def get_products_by_company(user:get_current_user,db:Session):
    products = db.query(Product).join(Company,Company.id==Product.company_id).filter(Company.id==user.company_id).all()
    company_pids = {p.id for p in products}

    return company_pids
