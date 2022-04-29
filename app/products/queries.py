from typing import List, Optional, Union
from uuid import UUID

from flask import abort

from config import Config

from .models import Product, db


def get_product(product_id: Union[UUID, str]) -> Optional[Product]:
    product = db.session.query(Product).get(product_id)
    if product is None:
        abort(404)
    return product


def get_products(page, items_per_page=Config.PAGE_SIZE) -> List[Product]:
    return (
        db.session.query(Product)
        .filter(Product.stock != 0)
        .order_by(Product.title)
        .paginate(page=page, per_page=items_per_page)
        .items
    )
