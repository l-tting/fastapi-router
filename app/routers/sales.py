from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas
from database import get_db
from auth import get_current_user

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
def make_sale(request: schemas.Sale, user=Depends(get_current_user), db: Session = Depends(get_db)):
    # Fetch the product that is being sold
    product = db.query(models.Product).filter(models.Product.id == request.pid).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Fetch the user who is making the sale
    user = db.query(models.User).filter(models.User.id == user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if there is enough stock for the sale
    if product.stock_quantity < request.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock available")

    # Create a new sale record
    new_sale = models.Sale(pid=request.pid, user_id=user.id, quantity=request.quantity)
    product.stock_quantity -= request.quantity  # Reduce stock by the quantity sold

    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)

    return {"message": "Sale made successfully", "sale_id": new_sale.id}
@router.get("/", status_code=status.HTTP_200_OK)
def fetch_sales(user=Depends(get_current_user), db: Session = Depends(get_db)):
    # Fetch all sales data and join with the Product table to access selling_price
    sales = db.query(models.Sale).join(models.Product).join(models.User).all()


    sales_data = []
    for sale in sales:
        amount = sale.quantity * sale.product.selling_price 
        sales_data.append({
            "id": sale.id,
            "pid": sale.pid,  
            "user_id": sale.user_id,
            "product_name": sale.product.name, 
            "quantity": sale.quantity,
            "amount": amount,  
            "created_at": sale.created_at
        })

    return {"sales_data": sales_data}


@router.get("/{sale_id}", status_code=status.HTTP_200_OK)
def fetch_sale(sale_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):

    sale = db.query(models.Sale).join(models.User).join(models.Product).filter(models.Sale.id == sale_id).first()
    amount = sale.quantity * sale.product.selling_price

    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")

    return {
        "id": sale.id,
        "pid": sale.pid,
        "user_id": sale.user_id,
        "product_name": sale.product.name,
        "quantity": sale.quantity,
        'amount':amount
    }

@router.put("/{sale_id}", status_code=status.HTTP_202_ACCEPTED)
def update_sale(sale_id: int, request: schemas.Sale, user=Depends(get_current_user), db: Session = Depends(get_db)):
    # Fetch the sale to be updated
    sale = db.query(models.Sale).filter(models.Sale.id == sale_id).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")

    # Fetch the product associated with the sale
    product = db.query(models.Product).filter(models.Product.id == sale.pid).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")


    quantity_difference = request.quantity - sale.quantity
    sale.quantity = request.quantity
    product.stock_quantity -= quantity_difference  # Update stock quantity based on the new sale quantity

    db.commit()

    return {"message": "Sale updated successfully"}

@router.get("/user/{user_id}", status_code=status.HTTP_200_OK)
def fetch_sales_by_user(user_id: int, db: Session = Depends(get_db)):

    sales = db.query(models.Sale).filter(models.Sale.user_id == user_id).join(models.User).all()

    if not sales:
        raise HTTPException(status_code=404, detail="No sales found for this user")

    return [{
        "id": sale.id,
        "pid": sale.pid,
        "user_id": sale.user_id,
        "first_name": sale.user.first_name,
        "quantity": sale.quantity
    } for sale in sales]
