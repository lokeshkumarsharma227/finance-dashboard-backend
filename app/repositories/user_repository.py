from typing import Optional,List
from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.models.user import User,UserRole
from app.schemas.user import UserUpdate

# Extends BaseRepository with user-specific queries.
# get_by_email is called on every login.
# update uses exclude_unset so only sent fields are changed.

class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    def get_by_email(self,db:Session,email:str)->Optional[User]:
         return db.query(User).filter(User.email == email).first()

    def get_by_role(self,db:Session,role:UserRole)->List[User]:
        return db.query(User).filter(User.role == role).all()

    def update(self, db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
        user = self.get_by_id(db, user_id)        
        if not user:                                 
            return None
        update_data = user_update.model_dump(exclude_unset=True)  
        for key, value in update_data.items():       
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
        return user                                  