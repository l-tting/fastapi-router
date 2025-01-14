from fastapi import APIRouter,status,Depends
import schemas,models
from sqlalchemy.orm import Session
from auth import get_current_user
from database import get_db
from routers.mpesa import *

router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED)
async def stk_push( db: Session = Depends(get_db)):
    phone_number = '254714056473'
    amount = '1'
    response =initiate_stk_push_request(phone_number,amount)
    stk = response.json()
    print("Received STK Push data:", stk) 
    # stk_push = models.STK_Push(
    #     merchant_request_id=stk.merchant_request_id,  
    #     checkout_request_id=stk.checkout_request_id,
    #     transaction_id = stk.transaction_id,
    #     amount=stk.amount,
    #     phone=stk.phone
    # )
    # db.add(stk_push)
    # db.commit()
    # db.refresh(stk_push)

    return {"Message": "Push added successfully"}



@router.get('/checker/',status_code=status.HTTP_200_OK)
async def get_stk_push_record(mrid:str,cid:str,user=Depends(get_current_user),db:Session=Depends(get_db)):

        stk_push_record = db.query(models.STK_Push).filter(models.STK_Push.merchant_request_id==mrid,models.STK_Push.checkout_request_id==cid).first()

        return {"STK Record": stk_push_record}
   