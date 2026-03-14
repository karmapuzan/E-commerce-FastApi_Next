from datetime import datetime, timedelta, timezone
from traceback import print_tb
from typing import Optional, Annotated
from pydantic import ValidationError


from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status

from sqlalchemy.orm import Session
from src.core.config import settings
from src.core.security import oauth2_scheme, pwd_context
from src.db.database import get_db
from src.models.users import User as UserModel

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="🕵️‍♂️ Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def authenticate_user(
    email: str,
    password: str,
    db: Session = Depends(get_db),
):
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user:
        return False
    if not pwd_context.verify(password, user.password_hash):  # type: ignore
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update(
        {
            "exp": expire,
            "sub": str(data.get("sub")),
            "type": "access",
        }
    )
    encoded = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id = payload.get("sub")
        token_type = payload.get("type")

        if user_id is None:
            raise credentials_exception

        if token_type != "access":
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if user is None:
        raise credentials_exception

    return user


def get_current_active_user(
    current_user: Annotated[UserModel, Depends(get_current_user)],
):
    if not current_user.is_active:  # pyright: ignore[reportGeneralTypeIssues]
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive User"
        )

    return current_user


def validate_refresh_token(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id = payload.get("sub")
        role = payload.get("role")

        if user_id is None or role is None:
            raise credentials_exception
    except (JWTError, ValidationError):
        raise credentials_exception

    user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if user is None:
        raise credentials_exception

    return user, token


class RoleChecker:
    def __init__(self, allowed_roles):
        self.allowed_roles = allowed_roles

    def __call__(self, user: Annotated[UserModel, Depends(get_current_active_user)]):
        if user.role.value in self.allowed_roles:
            return True
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You don't have enough permissions",
        )
