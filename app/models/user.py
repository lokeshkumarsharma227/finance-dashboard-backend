from sqlalchemy import Column,Integer,String,Boolean,DateTime,Enum
from sqlalchemy.sql import func
from enum import Enum as PyEnum
from app.models.base import Base
from sqlalchemy.orm import relationship

class UserRole(str,PyEnum):
    VIEWER="viewer"
    ADMIN="admin"
    ANALYST="analyst"


class User(Base):
    __tablename__ = "users"
    id= Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False,unique=True, index=True)
    hashed_password = Column(String,nullable=False)
    role = Column(Enum(UserRole), default=UserRole.VIEWER)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime,  server_default=func.now())
    updated_at = Column(DateTime,  onupdate=func.now())
    records = relationship("FinanceRecord", back_populates="owner")

    