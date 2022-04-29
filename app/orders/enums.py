from enum import Enum


class OrderStatusEnum(Enum):
    INITIAL = "initial"
    PROCESSING = "processing"
    CANCELED = "canceled"
    DELIVERED = "delivered"
