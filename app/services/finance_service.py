from sqlalchemy.orm import Session
from app.repositories.finance_repository import FinanceRepository
from app.schemas.finance import FinanceRecordCreate, FinanceRecordUpdate  
from app.models.finance import FinanceRecord ,TransactionType
from app.core.exceptions import NotFoundException, ForbiddenException
from typing import List, Optional
from datetime import date


class FinanceService:
    def __init__(self, finance_repo: FinanceRepository):
        self.finance_repo = finance_repo


   
    def create_record(self, db: Session, user_id: int, record_data: FinanceRecordCreate) -> FinanceRecord:
        record_dict = record_data.model_dump()
        record_dict["user_id"] = user_id

        return self.finance_repo.create(db, record_dict)


    
    def get_record_by_id(self, db: Session, record_id: int) -> FinanceRecord :
        record = self.finance_repo.get_by_id(db, record_id)
        if not record:
            raise NotFoundException("Record not found")
        return record


   
    def get_user_records(self, db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[FinanceRecord ]:
        return self.finance_repo.get_by_user(db, user_id, skip, limit)


    
    def get_filtered_records(self,db: Session,user_id: int,transaction_type: Optional[TransactionType] = None,
        category: Optional[str] = None,start_date: Optional[date] = None,end_date: Optional[date] = None) -> List[FinanceRecord ]:
        return self.finance_repo.get_by_filters( db,user_id,transaction_type,category,start_date,end_date)


   
    def update_record(self,db: Session,user_id: int,record_id: int,record_update: FinanceRecordUpdate) ->FinanceRecord :

        record = self.get_record_by_id(db, record_id)
        if record.user_id != user_id:
            raise ForbiddenException("Not your record")
        
        return self.finance_repo.update(db, record_id, record_update)


    
    def delete_record(self, db: Session, user_id: int, record_id: int) -> FinanceRecord :
        record = self.get_record_by_id(db, record_id)

        if record.user_id != user_id:
            raise ForbiddenException("Not your record")

        return self.finance_repo.delete(db, record_id)