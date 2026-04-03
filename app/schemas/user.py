from pydantic import BaseModel,EmailStr
from typing import Optional
from app.models.user import UserRole
from pydantic import ConfigDict

class UserBase(BaseModel):
    full_name:str
    email:EmailStr

class UserCreate(UserBase):
    password:str
    role: Optional[UserRole] = UserRole.VIEWER

class UserResponse(UserBase):
    id:int
    role:UserRole
    is_active:bool
    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    full_name: Optional[str] = None          
    role: Optional[UserRole] = None         
    is_active: Optional[bool] = None


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None




