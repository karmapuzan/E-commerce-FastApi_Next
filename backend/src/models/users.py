from db.database import Base
from sqlalchemy import BigInteger, Column, String, DateTime, func, Boolean, Enum
import uuid, enum


class UserRole(enum.Enum):
    CUSTOMER = "CUSTOMER"
    VENDOR = "VENDOR"
    ADMIN = "ADMIN"


class User(Base):
    __tablename__ = "users"

    uid = Column(
        String,
        primary_key=True,
        index=True,
        default=lambda: str(uuid.uuid4()),
        unique=True,
    )
    role = Column(Enum(UserRole), default=UserRole.CUSTOMER)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    phone = Column(BigInteger, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    refresh_token = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    update_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
