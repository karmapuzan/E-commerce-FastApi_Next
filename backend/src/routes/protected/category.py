from email.policy import HTTP
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError
from slugify import slugify

from src.core.auth import get_current_active_user
from src.db.database import get_db
from src.models.category import Category as CategoryModel
from src.schemas.category import Category
from src.services.role_checker import admin_vendor_only


router = APIRouter(
    prefix="",
    tags=["category"],
    dependencies=[
        Depends(get_current_active_user),
        Depends(admin_vendor_only),
    ],
)


@router.post("/category")
def create_category(
    category: Category,
    db: Annotated[CategoryModel, Depends(get_db)],
):

    has_category = (
        db.query(CategoryModel).filter(CategoryModel.name == category.name).first()
    )

    if has_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Category already exist"
        )

    try:
        new_category = CategoryModel(
            name=category.name,
            slug=slugify(str(category.name)),
            parent_id=category.parent_id,
        )
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return {
        "message": "Category has been successfully created",
        "data": new_category,
        "status": status.HTTP_201_CREATED,
    }
