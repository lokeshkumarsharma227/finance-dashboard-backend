from sqlalchemy.orm import Session
from typing import List,Optional
from datetime import date
from app.repositories.base import BaseRepository
from app.models.finance import FinanceRecord,TransactionType
from app.schemas.finance import FinanceRecordUpdate

# Extends BaseRepository with finance-specific queries.
# get_by_filters builds the query dynamically — handles all filter combinations
# without needing separate methods for each one.
class FinanceRepository(BaseRepository[FinanceRecord]):

    def __init__(self):
        super().__init__(FinanceRecord)

    def get_by_user(self,db:Session,user_id:int,skip:int=0,limit:int=100):
        return db.query(self.model).filter(FinanceRecord.user_id == user_id).offset(skip).limit(limit).all()
    
    def get_by_filters(self,db:Session,user_id:int,transaction_type: Optional[TransactionType] = None,category: Optional[str]=None, start_date: Optional[date] = None, end_date: Optional[date] = None):
        query = db.query(FinanceRecord).filter(FinanceRecord.user_id == user_id)
        if transaction_type:
            query = query.filter(FinanceRecord.transaction_type == transaction_type)
        if category:
            query = query.filter(FinanceRecord.category == category)
        if start_date:
            query = query.filter(FinanceRecord.date >= start_date)
        if end_date:
            query = query.filter(FinanceRecord.date <= end_date)
        return query.all()
    

    def update(self, db: Session, record_id: int, record_update: FinanceRecordUpdate) -> Optional[FinanceRecord]:
        record = self.get_by_id(db, record_id)
        if not record:
            return None
        update_data = record_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(record, key, value)
        db.commit()
        db.refresh(record)
        return record