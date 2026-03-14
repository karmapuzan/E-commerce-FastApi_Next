from sqlalchemy import Column, ForeignKey, String, DateTime, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
import uuid

from src.db.database import Base


class Category(Base):
    __tablename__ = "category"

    uid = Column(
        String,
        primary_key=True,
        index=True,
        default=lambda: str(uuid.uuid4()),
        unique=True,
    )
    name = Column(String(100), nullable=True)
    slug = Column(String(100), nullable=False)
    parent_id = Column(String, ForeignKey("category.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    parent: Mapped["Category"] = relationship(
        "Category", remote_side=[uid], back_populates="children"
    )
    children: Mapped[list["Category"]] = relationship(
        "Category", back_populates="parent"
    )
