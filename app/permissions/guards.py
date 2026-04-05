from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app.core.config import settings
from app.core.exceptions import ForbiddenException, NotFoundException
from app.db.session import get_db
from app.models.user import User, UserRole
from app.repositories.user_repository import UserRepository
# FastAPI dependency functions that protect routes.
# Each guard builds on the previous one — chain goes:
# get_current_user → get_current_active_user → get_current_admin
#
# Routes just declare which guard they need:
# current_user: User = Depends(get_current_admin)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
user_repo = UserRepository()

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = user_repo.get_by_id(db, int(user_id))
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    if not current_user.is_active:
        raise ForbiddenException("Inactive user")
    return current_user

def get_current_admin(
    current_user: User = Depends(get_current_active_user)
) -> User:
    if current_user.role != UserRole.ADMIN:
        raise ForbiddenException("Admin access required")
    return current_user



def get_current_analyst_or_admin(
    current_user: User = Depends(get_current_active_user)
) -> User:
    if current_user.role not in [UserRole.ANALYST, UserRole.ADMIN]:
        raise ForbiddenException("Analyst or Admin access required")
    return current_user


