import uuid

from sqlalchemy import Table
from sqlalchemy.dialects.postgresql import ENUM as EnumField
from sqlalchemy.dialects.postgresql.base import UUID

from ..database import db
from .enums import OrderStatusEnum


class OrderProduct(db.Model):
    __tablename__ = "order_products"
    order_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("products.id"), primary_key=True
    )
    product_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("orders.id"), primary_key=True
    )
    cost = db.Column(db.Integer, nullable=True)
    price = db.Column(db.Integer, nullable=True)
    count = db.Column(db.Integer, server_default="0", default=0, nullable=False)
    order = db.relationship("Order", back_populates="products")
    product = db.relationship("Product", back_populates="orders")


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    products = db.relationship(
        "OrderProduct", back_populates="order", cascade="all,delete"
    )
    status: OrderStatusEnum = db.Column(
        EnumField(OrderStatusEnum), default=OrderStatusEnum.INITIAL, nullable=False
    )
