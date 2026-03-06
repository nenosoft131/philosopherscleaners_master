from app.db.base import Base
from sqlalchemy import Column, Integer, ForeignKey, Enum, Float
from app.model.enums.order_enums import OrderType
from sqlalchemy.orm import relationship


class OrderItemORM(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)

    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)

    service_type = Column(Enum(OrderType), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)

    subtotal = Column(Float, nullable=False)

    order = relationship("OrderORM", back_populates="items")
