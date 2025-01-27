from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash
import models, schemas
from database import get_db
from auth import create_access_token
from datetime import timedelta

router = APIRouter()

@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)

def register_user(user: schemas.User, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed_password = generate_password_hash(user.password)
    new_user = models.User(
        company_id = user.company_id,
        full_name=user.full_name,
       
        email=user.email,
        phone_number=user.phone_number,
        password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully"}


@router.post("/login", status_code=status.HTTP_200_OK)
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    registered_user = db.query(models.User).filter(models.User.email == user.email).first()
    if registered_user is None or not check_password_hash(registered_user.password, user.password):
        raise HTTPException(status_code=404, detail="Invalid credentials")
    access_token = create_access_token(data={"user": user.email}, expires_delta=timedelta(hours=1))
    return {"access_token": access_token}


@router.get("/", status_code=status.HTTP_200_OK)
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return {"users": users}


