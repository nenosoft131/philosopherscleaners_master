from fastapi import APIRouter, Depends
from app.schema.user import CreateUserInput, LoginInput
from app.service.interfaces.user_service_interface import IUserService
from app.service.user.register_user import RegisterUser
from app.service.user.login_user import LoginUser
from app.utils.dependencies import get_user_service


router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/status")
def get_status():
    return {"Status": "Running"}


@router.post("/register")
async def get_registration(
    input: CreateUserInput, user_service: IUserService = Depends(get_user_service)
):

    register_service = RegisterUser(user_service)
    return await register_service.execute(input=input)


@router.post("/login")
async def login(
    input: LoginInput, user_service: IUserService = Depends(get_user_service)
):

    login_service = LoginUser(user_service)
    return await login_service.execute(input)
