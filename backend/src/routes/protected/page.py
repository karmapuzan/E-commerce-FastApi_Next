from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from src.core.auth import RoleChecker, get_current_active_user
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.models.page import Page as PageModel
from src.models.sections import Section as SectionModel
from src.models.users import User as UserModel
from src.schemas.section import PageWithSections

from src.core.auth import get_current_active_user
from src.services.role_checker import admin_vendor_only

router = APIRouter(
    prefix="",
    tags=["section"],
    dependencies=[
        Depends(get_current_active_user),
        Depends(admin_vendor_only),
    ],
)


@router.post("/page")
def create_page(
    title: str,
    db: Annotated[Session, Depends(get_db)],
):
    page = db.query(PageModel).filter(PageModel.title == title).first()
    if page:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Page is already created"
        )

    new_page = PageModel(slug=title.lower(), title=title)
    db.add(new_page)
    db.commit()

    return {
        "message": "Page has been successfully created",
        "data": {"title": title, "slug": title.lower()},
        "status": status.HTTP_201_CREATED,
    }


@router.post("/home")
def create_hero_banner(
    payload: PageWithSections,
    db: Annotated[Session, Depends(get_db)],
):

    page = db.query(PageModel).filter(PageModel.id == payload.page_data.id).first()
    print(page)
    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Page with title '{payload.page_data.id}' not found",
        )
    created_sections = []

    for section in payload.landing:
        exiting = (
            db.query(SectionModel)
            .filter(
                SectionModel.page_id == page.id,
                SectionModel.type == section.type,
                SectionModel.order == section.order,
            )
            .first()
        )

        if exiting:
            continue

        new_section = SectionModel(
            page_id=page.id,
            type=section.type,
            order=section.order,
            content=section.content.dict(),
        )

        db.add(new_section)
        created_sections.append(new_section)
    db.commit()

    return {
        "message": "Sections created successfully",
        "total_sections": len(created_sections),
        "status": status.HTTP_201_CREATED,
    }
