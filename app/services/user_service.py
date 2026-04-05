from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.models.user import User
from app.core.security import hash_password, verify_password
from app.core.exceptions import NotFoundException, BadRequestException
from typing import Optional, List

# All user business logic lives here.
# Routes call this — this calls the repository.
# Nothing in here touches SQLAlchemy directly.


class UserService:
    def __init__(self, user_repo:UserRepository):
        self.user_repo = user_repo

  
    def create_user(self, db: Session, user_data: UserCreate) -> User:

        existing_user = self.user_repo.get_by_email(db, user_data.email)
        if existing_user:
            raise BadRequestException("Email already registered")

       
        hashed = hash_password(user_data.password)

    
        user_dict = user_data.model_dump(exclude={"password"})
        user_dict["hashed_password"] = hashed

   
        return self.user_repo.create(db, user_dict)

   
    def get_user_by_id(self, db: Session, user_id: int) -> User:
        user = self.user_repo.get_by_id(db, user_id)
        if not user:
            raise NotFoundException("User not found")
        return user

  
    def get_all_users(self, db:Session,skip: int = 0, limit: int = 100)->List[User]:
        return self.user_repo.get_all(db, skip=skip, limit=limit)

 
    def update_user(self, db:Session, user_id: int, user_update: UserUpdate)-> User:
        user = self.user_repo.update(db, user_id, user_update)
        if not user:
            raise NotFoundException("User not found")
        return user

 
    def delete_user(self, db:Session,user_id: int)-> User:
        user = self.user_repo.delete(db, user_id)
        if not user:
            raise NotFoundException("User not found")
        return user

  
    def authenticate_user(self, db:Session,  email: str, password: str)->Optional[User]:
        user = self.user_repo.get_by_email(db, email)
        if not user:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        return user