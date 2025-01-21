from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func,Enum
from sqlalchemy.orm import relationship
from database import Base
import enum
# from database import Base

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    buying_price = Column(Integer, nullable=False)
    selling_price = Column(Integer, nullable=False)
    stock_quantity = Column(Integer, nullable=False)
    sales = relationship("Sale", back_populates='product')

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone_number = Column(String, nullable=False)
    password = Column(String,nullable=False)
    role = Column(String,nullable=False,default='user')
    sales = relationship("Sale", back_populates='user')

class Sale(Base):
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True)
    pid = Column(Integer, ForeignKey('products.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=func.now())
    product = relationship("Product", back_populates='sales')
    user = relationship("User", back_populates='sales')
    payment = relationship('Payment',back_populates='sale')



class Vendor(Base):
    __tablename__ = 'vendors'
    id = Column(Integer,primary_key=True)
    vendor_name = Column(String,nullable=False,unique=True)
    phone_number = Column(String,nullable=False,unique=True)
    email = Column(String,nullable = False, unique=True)
    address = Column(String,nullable=False)
    stock = relationship("Stock",back_populates='vendor')

class Stock(Base):
    __tablename__ = 'stock'
    id = Column(Integer,primary_key=True)
    product_name = Column(String,nullable=False)
    stock_count = Column(Integer,nullable=False)
    vendor_name = Column(String,ForeignKey('vendors.vendor_name'),nullable=False)
    created_at = Column(DateTime,default=func.now())
    vendor = relationship('Vendor',back_populates='stock')
    
    
class Payment(Base):
    __tablename__ = 'payments'
    payment_id = Column(String,primary_key=True)
    sale_id = Column(Integer,ForeignKey('sales.id'),nullable=False)
    amount = Column(Integer,nullable=False)
    mode = Column(String,nullable=False)
    transaction_code = Column(String,nullable=False)
    created_at = Column(DateTime,server_default=func.now())
    sale = relationship('Sale',back_populates='payment')


# The enum module is used to define an enumeration of possible values for a column
class MPESAStatus(str, enum.Enum):
    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'
    CANCELLED = 'cancelled'
    TIMEOUT = 'timeout'


class STK_Push(Base):
    __tablename__= 'stk_push'
    stk_id = Column(Integer,primary_key=True)
    merchant_request_id = Column(String,nullable=False)
    checkout_request_id = Column(String,nullable=False)
    amount = Column(Integer,nullable=False)
    phone = Column(String,nullable=False)
    status = Column(Enum(MPESAStatus, name='mpesa_status_enum'),
        default=MPESAStatus.PENDING,
        nullable=False
    )
    result_code = Column(String,nullable=True)
    result_desc = Column(String,nullable=True)
    created_at = Column(DateTime,server_default=func.now())

