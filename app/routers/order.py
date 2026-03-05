from fastapi import APIRouter


router = APIRouter(prefix="/order", tags=["order"])


@router.post("/place")
async def place_order():
    pass


@router.get("/orderlist")
async def get_order_list():
    pass
