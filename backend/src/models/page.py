import uuid
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from src.db.database import Base


class Page(Base):
    __tablename__ = "pages"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        unique=True,
    )
    slug = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=True)

    sections = relationship("Section", back_populates="page", order_by="Section.order")
