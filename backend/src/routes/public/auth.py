from datetime import timedelta
from sqlalchemy.orm import Session
from typing import Annotated

from fastapi import Depends, HTTPException, APIRouter, status
from fastapi.security import OAuth2PasswordRequestForm

from src.core.auth import authenticate_user, create_access_token
from src.models.users import User as UserModel
from src.schemas.users import Token
from src.db.database import get_db
from src.core.config import settings

from src.models.users import User as UserModel
from src.schemas.users import UserCreate
from src.core.security import hash_password

router = APIRouter(prefix="", tags=["auth"])


@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    user = authenticate_user(
        email=form_data.username,
        password=form_data.password,
        db=db,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": user.id},
        expires_delta=access_token_expires,
    )
    refresh_token = create_access_token(
        data={"sub": user.id},
        expires_delta=refresh_token_expires,
    )

    user.refresh_token = refresh_token  # type: ignore
    db.commit()
    db.refresh(user)

    return Token(
        msg="User has logged in",
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post("/register")
def register_user(user_data: UserCreate, db: Annotated[Session, Depends(get_db)]):
    user = db.query(UserModel).filter(UserModel.email == user_data.email).first()

    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="user already exist"
        )
    new_user = UserModel(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        phone=user_data.phone,
        password_hash=hash_password(user_data.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully", "data": new_user}


@router.post("/register-vendor")
def register_vendor(user_data: UserCreate, db: Annotated[Session, Depends(get_db)]):
    vendor = db.query(UserModel).filter(UserModel.email == user_data.email).first()

    if vendor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="user already exist"
        )

    new_vendor = UserModel(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        role="VENDOR",
        phone=user_data.phone,
        password_hash=hash_password(user_data.password),
    )

    db.add(new_vendor)
    db.commit()
    db.refresh(new_vendor)

    return {
        "message": "User created successfully",
        "status": status.HTTP_200_OK,
        "data": new_vendor,
    }
