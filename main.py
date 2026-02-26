import uvicorn
from fastapi import FastAPI
from app.routers.auth import router
from contextlib import asynccontextmanager
from app.db.session import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    print("Database initialized")
    yield
    # Shutdown logic (optional)
    print("Application shutting down")


app = FastAPI(
    title="Philosophers Cleaners API",
    version="1.0.0",
    description="philosophers cleaners backend",
    docs_url="/docs",  # Swagger
    redoc_url="/redoc",  # ReDoc
    lifespan=lifespan,
)

app.include_router(router=router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",  # file_name:app_instance
        host="0.0.0.0",
        port=8000,
        reload=False,  # remove in production
    )
