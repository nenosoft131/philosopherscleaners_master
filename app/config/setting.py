from pydantic_settings import BaseSettings


class Setting(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./test.db"
    SECRET_KEY: str = "9d261b1d61768b7b688b240029e451aaa28e2f67352c9f3d4d3f9ed7c0cb8855dd8077b1109b025ce55128d37846f009cc4bfde7d122ea25d0db15642a8147aa"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


def get_setting() -> Setting:
    return Setting()
