from typing import Optional

from pydantic import BaseModel, field_validator


class Category(BaseModel):
    name: str
    slug: Optional[str] = None
    parent_id: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes = True

    @field_validator("name", mode="after")
    def name_must_not_be_empty(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("Name must not be empty or whitespace")
        if len(v) < 2:
            raise ValueError("Name must be at least 2 characters long")
        if len(v) > 100:
            raise ValueError("Name must not exceed 100 characters")
        return v


class SubChildCategory(BaseModel):
    id: str
    name: str
    slug: str

    class Config:
        from_attributes = True


class ChildCategory(BaseModel):
    id: str
    name: str
    slug: str
    children: list[SubChildCategory] = []

    class Config:
        from_attributes = True


class CategoryResponse(BaseModel):
    id: str
    name: str
    slug: str
    children: list[ChildCategory] = []

    class Config:
        from_attributes = True


class MetaResponse(BaseModel):
    total: int
    page: int
    page_size: int


class CategoryListResponse(BaseModel):
    message: str
    data: list[CategoryResponse]
    status: int
    meta: MetaResponse
