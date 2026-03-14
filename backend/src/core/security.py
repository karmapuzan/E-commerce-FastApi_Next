from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(hashed_password: str, password: str):
    return pwd_context.verify(hashed_password, password)
