from fastapi import Request
from starlette.responses import JSONResponse
import logging
import jwt  # pip install PyJWT
import os

logger = logging.getLogger("auth")
logging.basicConfig(level=logging.INFO)

# Secret for JWT (in production, keep in env variable!)
JWT_SECRET = os.getenv("JWT_SECRET", "mysecret")
JWT_ALGORITHM = "HS256"

# Sample API keys
VALID_API_KEYS = {"12345", "abcdef"}

# Public routes that don't require auth
PUBLIC_ROUTES = {"/public", "/status"}


async def auth_middleware(request: Request, call_next):
    path = request.url.path

    # Skip auth for public routes
    if path in PUBLIC_ROUTES:
        return await call_next(request)

    auth_header = request.headers.get("Authorization")
    api_key = request.headers.get("X-API-KEY")

    user_info = None

    # 1️⃣ Check API Key
    if api_key:
        if api_key in VALID_API_KEYS:
            user_info = {"api_key": api_key}
        else:
            logger.warning(
                f"Unauthorized API key attempt: {api_key} from {request.client.host}"
            )
            return JSONResponse(status_code=401, content={"error": "Invalid API Key"})

    # 2️⃣ Check JWT
    elif auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            user_info = payload  # attach decoded payload
        except jwt.ExpiredSignatureError:
            return JSONResponse(status_code=401, content={"error": "Token expired"})
        except jwt.InvalidTokenError:
            return JSONResponse(status_code=401, content={"error": "Invalid token"})
    else:
        return JSONResponse(
            status_code=401, content={"error": "Authorization required"}
        )

    # Attach user info to request.state
    request.state.user = user_info

    response = await call_next(request)
    return response
