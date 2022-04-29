import uuid
from typing import Optional

import pydantic

from .enums import ProductStatusEnum


class ProductInputSchema(pydantic.BaseModel):
    title: str
    cost: pydantic.PositiveInt
    price: pydantic.PositiveInt
    stock: pydantic.PositiveInt


class ProductPatchSchema(pydantic.BaseModel):
    cost: Optional[pydantic.PositiveInt]
    price: Optional[pydantic.PositiveInt]
    stock: Optional[pydantic.PositiveInt]


class ProductOutputSchema(ProductInputSchema):
    id: uuid.UUID
    status: ProductStatusEnum

    class Config:
        orm_mode = True
        use_enum_values = True
