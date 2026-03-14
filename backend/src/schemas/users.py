from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    first_name: str
    last_name: str
    email: EmailStr
    phone: int
    password: str = Field(min_length=5)


class UserResponse(UserBase):
    id: str
    first_name: str
    last_name: str
    is_active: bool
    phone: int
    role: str

    class Config:
        from_attribute = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    msg: str
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
