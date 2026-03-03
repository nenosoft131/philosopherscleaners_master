from app.service.interfaces.jwt_token_interface import ITokenGeneration
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from app.config.setting import get_setting
from typing import Optional

settings = get_setting()


class TokenGen(ITokenGeneration):
    @staticmethod
    def generate_token(data: dict, expires_delta: Optional[int] = None) -> str:

        if not isinstance(data, dict):
            raise TypeError(
                f"Token data must be a dictionary, got {type(data).__name__}"
            )
        try:
            to_encode = data.copy()
            expire_minutes = (
                expires_delta
                if expires_delta is not None
                else settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
            expire_time = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)
            to_encode.update({"exp": expire_time})

            return jwt.encode(
                to_encode, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM
            )
        except TypeError as e:
            raise ValueError(f"Token payload contains non-serializable values: {e}")
        except jwt.PyJWTError as e:
            raise ValueError(f"Failed to generate JWT token: {e}")

    @staticmethod
    def decode_access_token(token: str):
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            return payload
        except JWTError:
            return None
