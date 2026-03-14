import uuid, enum
from src.db.database import Base
from sqlalchemy import Column, ForeignKey, String, DateTime, Float, func, Enum
from sqlalchemy.orm import relationship


class ProductStatus(enum.Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"


class Product(Base):
    __tablename__ = "products"

    uid = Column(
        String,
        primary_key=True,
        index=True,
        default=lambda: str(uuid.uuid4()),
        unique=True,
    )
    vendor_id = Column(String, ForeignKey("vendors.id"), nullable=False)
    category_id = Column(String, ForeignKey("category.id"), nullable=False)
    name = Column(String(150), nullable=False)
    slug = Column(String(150), nullable=False)
    description = Column(String, nullable=False)
    base_price = Column(Float, nullable=False)
    status = Column(Enum(ProductStatus), default=ProductStatus.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    update_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    vendor = relationship("Vendor", back_populates="products")
    category = relationship("Category", back_populates="products")
