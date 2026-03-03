from enum import Enum


class PaymentStatus(str, Enum):
    unpaid = "unpaid"
    paid = "paid"
    refunded = "refunded"


class PaymentMethod(str, Enum):
    cash = "cash"
    card = "card"
    online = "online"
