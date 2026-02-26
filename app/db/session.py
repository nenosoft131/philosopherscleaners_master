from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config.setting import get_setting
from app.db.base import Base


setting = get_setting()


async def init_db():
    """
    Initialize the database: create all tables if they don't exist.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print(" Database initialized (tables created if missing)")


engine = create_async_engine(setting.DATABASE_URL)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_db_session():
    async with AsyncSessionLocal() as session:
        yield session
