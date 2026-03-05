import uvicorn
from fastapi import FastAPI
from app.routers.auth import router
from contextlib import asynccontextmanager
from app.db.session import init_db
from fastapi.middleware.cors import CORSMiddleware


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
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.include_router(router=router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",  # file_name:app_instance
        host="0.0.0.0",
        port=8000,
        reload=False,  # remove in production
    )
