# from sqlalchemy import Integer, ForeignKey, Column, DateTime, Enum, Text, Float
# from app.model.enums.order_enums import OrderStatus
# from app.db.base import Base
# from sqlalchemy.orm import relationship
# from sqlalchemy.sql import func


# class OrderORM(Base):
#     __tablename__ = "orders"

#     id = Column(Integer, primary_key=True, index=True)

#     customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)

#     status = Column(Enum(OrderStatus), default=OrderStatus.pending, nullable=False)

#     pickup_address = Column(Text, nullable=True)
#     delivery_address = Column(Text, nullable=True)

#     pickup_date = Column(DateTime(timezone=True), nullable=True)
#     delivery_date = Column(DateTime(timezone=True), nullable=True)

#     total_amount = Column(Float, nullable=False, default=0.0)

#     created_at = Column(DateTime(timezone=True), server_default=func.now())
#     updated_at = Column(DateTime(timezone=True), onupdate=func.now())

#     customer = relationship("UserORM", back_populates="orders")
#     items = relationship("OrderItemORM", back_populates="order", cascade="all, delete")
#     payment = relationship("PaymentORM", back_populates="order", uselist=False)
