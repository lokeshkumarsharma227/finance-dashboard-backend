from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.db.session import get_db
from app.services.finance_service import FinanceService
from app.repositories.finance_repository import FinanceRepository
from app.schemas.finance import FinanceRecordCreate, FinanceRecordUpdate, FinanceRecordResponse
from app.models.finance import TransactionType
from app.models.user import User
from app.permissions.guards import (
    get_current_active_user,
    get_current_admin,
    get_current_analyst_or_admin
)

router = APIRouter(prefix="/records", tags=["Finance Records"])
finance_service = FinanceService(FinanceRepository())

@router.post("/", response_model=FinanceRecordResponse)
def create_record(
    record_data: FinanceRecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_analyst_or_admin)
):
    return finance_service.create_record(db, current_user.id, record_data)


@router.get("/", response_model=List[FinanceRecordResponse])
def get_records(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return finance_service.get_user_records(db, current_user.id, skip, limit)


@router.get("/filter", response_model=List[FinanceRecordResponse])
def filter_records(
    transaction_type: Optional[TransactionType] = None,
    category: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return finance_service.get_filtered_records(
        db, current_user.id,
        transaction_type, category,
        start_date, end_date
    )


@router.get("/{record_id}", response_model=FinanceRecordResponse)
def get_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return finance_service.get_record_by_id(db, record_id)


@router.patch("/{record_id}", response_model=FinanceRecordResponse)
def update_record(
    record_id: int,
    record_update: FinanceRecordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_analyst_or_admin)
):
    return finance_service.update_record(
        db, current_user.id, record_id, record_update, current_user.role
    )




@router.delete("/{record_id}", response_model=FinanceRecordResponse)
def delete_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    return finance_service.delete_record(
        db, current_user.id, record_id, current_user.role  
    )