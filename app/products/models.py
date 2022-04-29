import uuid

from sqlalchemy.dialects.postgresql import ENUM as EnumField
from sqlalchemy.dialects.postgresql.base import UUID

from ..database import db
from .enums import ProductStatusEnum


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String, nullable=False)
    cost = db.Column(db.Integer, server_default="0", default=0, nullable=False)
    price = db.Column(db.Integer, server_default="0", default=0, nullable=False)
    stock = db.Column(db.Integer, server_default="0", default=0, nullable=False)
    status: ProductStatusEnum = db.Column(
        EnumField(ProductStatusEnum), default=ProductStatusEnum.NORMAL, nullable=False
    )
    orders = db.relationship(
        "OrderProduct", back_populates="product", cascade="all,delete"
    )
