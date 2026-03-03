from app.service.interfaces.password_hasher_interface import IPasswordHasher
import bcrypt
from typing import Final

BCRYPT_ROUNDS: Final[int] = 12


class HashingService(IPasswordHasher):
    @staticmethod
    def get_hashed_password(password: str) -> str:
        if not isinstance(password, str):
            raise TypeError(
                f"Invalid password type: expected str, got {type(password).__name__}"
            )
        if not password:
            raise ValueError("Password cannot be empty")

        pwd_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt(rounds=BCRYPT_ROUNDS)
        hashed = bcrypt.hashpw(pwd_bytes, salt=salt)
        return hashed.decode("utf-8")

    @staticmethod
    def validate_password(plain_password: str, hash_password: str):
        if not isinstance(hash_password, str):
            raise TypeError(
                f"Invalid password type: expected str, got {type(hash_password).__name__}"
            )
        if not isinstance(plain_password, str):
            raise TypeError(
                f"Invalid password type: expected str, got {type(plain_password).__name__}"
            )
        try:
            hash_encode = hash_password.encode("utf-8")
            plain_encode = plain_password.encode("utf-8")
            return bcrypt.checkpw(plain_encode, hashed_password=hash_encode)
        except (ValueError, TypeError, bcrypt.errors.InvalidSalt) as e:
            raise ValueError("Invalid hashed password format") from e
