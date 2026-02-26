from pydantic_settings import BaseSettings


class Setting(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./test.db"


def get_setting() -> Setting:
    return Setting()
