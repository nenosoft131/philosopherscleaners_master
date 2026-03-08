from app.service.interfaces.order_interface import IOder
from app.db.session import AsyncSession
from app.model.order import OrderORM
from sqlalchemy.exc import IntegrityError


class OrderService(IOder):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def place_order(self, order: OrderORM):
        try:
            self._session.add(order)
            await self._session.commit()
            await self._session.refresh(order)
            return order
        except IntegrityError:
            raise ValueError("Order already exist")
