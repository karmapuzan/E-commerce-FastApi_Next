import uuid
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from src.db.database import Base


class Section(Base):
    __tablename__ = "sections"

    id = Column(
        String,
        primary_key=True,
        index=True,
        default=lambda: str(uuid.uuid4()),
        unique=True,
    )
    page_id = Column(String, ForeignKey("pages.id"), nullable=False)
    type = Column(String, nullable=False)
    content = Column(JSONB, nullable=False)
    order = Column(Integer, nullable=False)

    page = relationship("Page", back_populates="sections")
