from fastapi import APIRouter, Depends
from app.schema.user import CreateUserInput, LoginInput
from app.service.interfaces.user_service_interface import IUserService
from app.service.interfaces.password_hasher_interface import IPasswordHasher
from app.service.userservice.user_service import UserService
from app.db.session import AsyncSession, get_async_db_session
from app.service.userservice.register_user import RegisterUser
from app.service.userservice.login_user import LoginUser


router = APIRouter(prefix="/auth", tags=["auth"])


def get_user_service(
    session: AsyncSession = Depends(get_async_db_session),
) -> IUserService:
    return UserService(session=session)


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
