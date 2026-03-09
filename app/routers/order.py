from fastapi import APIRouter
from app.schema.order import Order

router = APIRouter(prefix="/order", tags=["order"])


@router.post("/place")
async def place_order(order: Order):
    pass


@router.get("/orderlist")
async def get_order_list():
    pass
