from app.db.session import AsyncSession, get_async_db_session
from fastapi import Depends
from app.service.interfaces.user_service_interface import IUserService

# from app.service.interfaces.order_interface import IOder
from app.service.user.user_service import UserService
# from app.service.order.order_service import OrderService


def get_user_service(
    session: AsyncSession = Depends(get_async_db_session),
) -> IUserService:
    return UserService(session=session)


# def get_order_service(
#     session: AsyncSession = Depends(get_async_db_session),
# ) -> IOder:
#     return OrderService(session=session)
