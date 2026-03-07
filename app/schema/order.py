from pydantic import BaseModel
from app.model.enums.order_enums import OrderStatus, OrderType
from datetime import datetime


class Order(BaseModel):
    customer_id = int
    order_type = OrderType
    cloth_type = str
    quantity = int
    size = 1
    pickup_address = str
    status = OrderStatus
