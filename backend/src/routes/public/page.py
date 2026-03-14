from typing import Annotated

from fastapi import APIRouter, Depends, status
from src.core.security import oauth2_scheme
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.models.page import Page as PageModel
from src.models.sections import Section as SectionModel
from src.schemas.section import SectionResponse


router = APIRouter(prefix="", tags=["section"])


@router.get("/page")
def get_page_content(db: Annotated[Session, Depends(get_db)]):
    get_data = db.query(PageModel).all()
    return get_data


@router.get("/section", response_model=SectionResponse)
def get_section_content(db: Annotated[Session, Depends(get_db)]):
    sections = db.query(SectionModel).all()
    return {
        "message": "Data fetched successfully",
        "data": sections,
        "status": status.HTTP_200_OK,
    }
