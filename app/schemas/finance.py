from pydantic import BaseModel,ConfigDict
from app.models.finance import TransactionType
from typing import Optional
from  datetime import datetime,date



class FinanceRecordBase(BaseModel):
    amount:float
    date:date
    description:Optional[str]=None
    transaction_type:TransactionType
    category:str

class FinanceRecordCreate(FinanceRecordBase):
    pass

class FinanceRecordUpdate(BaseModel):
    amount :Optional[ float]=None
    transaction_type : Optional[TransactionType]=None
    category:Optional[str]=None
    date:Optional[date]=None
    description : Optional[str] = None

class FinanceRecordResponse(FinanceRecordBase):
    id:int
    user_id:int
    created_at:datetime
    model_config=ConfigDict(from_attributes=True)