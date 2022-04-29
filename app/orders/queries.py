from typing import List, Optional, Union
from uuid import UUID

from flask import abort

from app.products.models import Product
from config import Config

from .enums import OrderStatusEnum
from .models import Order, OrderProduct, db


def get_order(order_id: Union[UUID, str]) -> Optional[Order]:
    order = db.session.query(Order).get(order_id)
    if order is None:
        abort(404)
    return order


def get_current_order() -> Order:
    order = (
        db.session.query(Order)
        .filter(Order.status == OrderStatusEnum.INITIAL)
        .one_or_none()
    )
    if not order:
        order = Order()
        db.session.add(order)
        db.session.commit()
    return order


def get_orders(page, items_per_page=Config.PAGE_SIZE) -> List[Order]:
    return (
        db.session.query(Order)
        .filter(Order.stock != 0)
        .order_by(Order.title)
        .paginate(page=page, per_page=items_per_page)
        .items
    )


def get_product_from_order(order: Order, product: Product) -> Optional[OrderProduct]:
    try:
        return next(prod for prod in order.products if prod.product == product)
    except StopIteration:
        return None
