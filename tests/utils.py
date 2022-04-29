import random
from typing import List
from app.products.models import Product


def generate_products(number: int) -> List[Product]:
    return [Product(
        title=f"product-{i}",
        cost=random.randint(10, 100),
        price=random.randint(100, 150),
        stock=random.randint(0, 50),
    ) for i in range(number)]
