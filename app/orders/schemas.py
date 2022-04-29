import uuid
from typing import List

import pydantic

from app.products.schemas import ProductOutputSchema

from .enums import OrderStatusEnum


class AddProductSchema(pydantic.BaseModel):
    product_id: uuid.UUID
    count: pydantic.NonNegativeInt


class OrderProductSchema(pydantic.BaseModel):
    product: ProductOutputSchema
    count: int
    # TODO add count validator

    class Config:
        orm_mode = True


class OrderSchema(pydantic.BaseModel):
    products: List[OrderProductSchema]
    status: OrderStatusEnum

    class Config:
        orm_mode = True
