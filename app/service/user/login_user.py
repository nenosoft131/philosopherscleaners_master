from app.service.interfaces.user_service_interface import IUserService
from app.schema.user import LoginInput, LoginOutput
from app.service.security.hasher import HashingService
from app.service.security.jwt_token import TokenGen
from fastapi import HTTPException, status


class LoginUser:
    def __init__(self, user_service: IUserService) -> None:
        self._user_service = user_service

    async def execute(self, input: LoginInput):

        user = await self._user_service.get_by_email(input.email)

        if not user or not HashingService.validate_password(
            input.password, user.hashed_password
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        token_data = {"sub": user.email, "role": user.role}
        access_token = TokenGen.generate_token(token_data)
        return LoginOutput(access_token=access_token)
