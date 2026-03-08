from app.service.interfaces.order_interface import IOder
from app.schema.order import Order
from app.model.order import OrderORM


class PlaceOrder:
    def __init__(self, order_service: IOder) -> None:
        self._order_service = order_service

    def create_order(self, order: Order):
        order_orm = OrderORM()
