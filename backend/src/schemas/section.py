from typing import List

from pydantic import BaseModel


class PageData(BaseModel):
    id: str

    class Config:
        from_attributes = True


class Image(BaseModel):
    alt: str
    url: str

    class Config:
        from_attributes = True


class Section(BaseModel):
    type: str
    headline: str
    subtitle: str
    image: Image

    class Config:
        from_attributes = True


class LandingSectionContent(BaseModel):
    hero: Section

    class Config:
        from_attributes = True


class LandingSection(BaseModel):
    type: str
    order: int
    content: LandingSectionContent

    class Config:
        from_attributes = True


class PageWithSections(BaseModel):
    page_data: PageData
    landing: List[LandingSection]


class SectionResponse(BaseModel):
    message: str
    data: List[LandingSection]

    class Config:
        from_attributes = True
        orm_mode = True
