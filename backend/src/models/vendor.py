import uuid
from src.db.database import Base
from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    DateTime,
    func,
)
from sqlalchemy.orm import relationship


class Vendor(Base):
    __tablename__ = "vendors"

    id = Column(
        String,
        primary_key=True,
        index=True,
        default=lambda: str(uuid.uuid4()),
        unique=True,
    )
    user_id = Column(String, ForeignKey("users.uid"), nullable=False)
    store_name = Column(String(150), nullable=False)
    store_slug = Column(String(150), nullable=False)
    description = Column(String, nullable=False)
    logo = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    update_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="Vendor")
