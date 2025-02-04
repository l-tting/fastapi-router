from fastapi import APIRouter,HTTPException,Depends
from sqlalchemy.orm import Session
from schemas import TierCreate
from models import Tier
from database import get_db

router = APIRouter()

@router.post('/')
def add_a_tier(request:TierCreate,db:Session=Depends(get_db)):
    try: 

        new_tier = Tier(name=request.name,description=request.description,amount=request.amount)
        db.add(new_tier)
        db.commit()
        db.refresh(new_tier)

        return {"Tier message":"Tier added succesfully"}

    except Exception as e:
        raise HTTPException(status_code=500,detail=f'{e}')



