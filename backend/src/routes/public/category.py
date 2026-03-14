from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.models import page
from src.models.category import Category as CategoryModel
from src.db.database import get_db
from src.schemas.category import CategoryListResponse

router = APIRouter(prefix="", tags=["category"])


@router.get("/category", response_model=CategoryListResponse)
def get_category_content(
    db: Annotated[Session, Depends(get_db)],
    page: int = 1,
    page_size: int = 10,
):
    """
    Retrieve a list of categories with their children.

    Args:
        db (Session, optional): The database session. Defaults to Depends(get_db).
        page (int, optional): The page number. Defaults to 1.
        page_size (int, optional): The number of items per page. Defaults to 10.

    Returns:
            List[CategoryResponse]: A list of categories with their children.
    """
    total = db.query(CategoryModel).count()
    try:
        get_data = (
            db.query(CategoryModel)
            .filter(CategoryModel.parent_id == None)
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    if not get_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )

    return {
        "message": "Category has been successfully fetched",
        "status": status.HTTP_200_OK,
        "data": get_data,
        "meta": {
            "total": total,
            "page": page,
            "page_size": page_size,
        },
    }


@router.get("/category/{id}")
def get_category_content_by_id(id: str, db: Annotated[CategoryModel, Depends(get_db)]):
    get_data = db.query(CategoryModel).filter(CategoryModel.id == id).first()

    if not get_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )

    return {
        "message": "Category has been successfully fetched",
        "status": status.HTTP_200_OK,
        "data": get_data,
    }
