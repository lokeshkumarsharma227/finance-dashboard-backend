from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.finance import FinanceRecord, TransactionType
from app.schemas.dashboard import DashboardSummary, CategorySummary
from typing import List




class DashboardService:
    def get_summary(self, db: Session, user_id: int) -> DashboardSummary:

        
        total_income = db.query(func.sum(FinanceRecord.amount)) \
            .filter(
                FinanceRecord.user_id == user_id,
                FinanceRecord.transaction_type == TransactionType.INCOME
            ).scalar() or 0.0

       
        total_expenses = db.query(func.sum(FinanceRecord.amount)) \
            .filter(
                FinanceRecord.user_id == user_id,
                FinanceRecord.transaction_type == TransactionType.EXPENSE
            ).scalar() or 0.0

        
        net_balance = total_income - total_expenses

        
        category_results = db.query(
            FinanceRecord.category,
            func.sum(FinanceRecord.amount)
        ).filter(
            FinanceRecord.user_id == user_id
        ).group_by(FinanceRecord.category).all()

        category_totals = [
            CategorySummary(category=cat, total=total)
            for cat, total in category_results
        ]

        
        total_records = db.query(func.count(FinanceRecord.id)) \
            .filter(FinanceRecord.user_id == user_id) \
            .scalar() or 0

        
        return DashboardSummary(
            total_income=total_income,
            total_expenses=total_expenses,
            net_balance=net_balance,
            category_totals=category_totals,
            total_records=total_records
        )