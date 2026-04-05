from sqlalchemy import Column,Integer,Float,String,DateTime,Enum,Text,Date,ForeignKey
from sqlalchemy.sql import func
from enum import Enum as PyEnum
from app.models.base import Base
from sqlalchemy.orm import relationship

# Defines the 'finance_records' table.
# Every record belongs to exactly one user via the user_id foreign key.
class TransactionType(str,PyEnum):
    INCOME="income"
    EXPENSE="expense"

class FinanceRecord(Base):
    __tablename__="finance_records"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    category = Column(String(100),nullable=False)
    date = Column(Date,nullable=False)
    description = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"),nullable=False, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    owner = relationship("User", back_populates="records")