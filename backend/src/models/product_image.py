import uuid
from src.db.database import Base
from sqlalchemy import Column, ForeignKey, String, Boolean, Integer
from sqlalchemy.orm import relationship


class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(
        String,
        primary_key=True,
        index=True,
        default=lambda: str(uuid.uuid4()),
        unique=True,
    )
    product_id = Column(String, ForeignKey("products.id"), nullable=False)
    image_url = Column(String, nullable=False)
    is_primary = Column(Boolean, default=True)
    sort_order = Column(Integer, nullable=True)
