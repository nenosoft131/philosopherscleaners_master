from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config.setting import get_setting


setting = get_setting()

engin = create_async_engine(setting.DATABASE_URL)
AsyncSessionLocal = sessionmaker(engin, class_=AsyncSession, expire_on_commit=False)


async def get_async_db_session():
    async with AsyncSessionLocal() as session:
        yield session
