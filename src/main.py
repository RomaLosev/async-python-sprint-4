from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse
from loguru import logger

from api import base
from core.config import BLOCKED_IPS, app_settings
from users.manager import auth_backend, fastapi_users
from users.schemas import UserCreate, UserRead

app = FastAPI(
    title=app_settings.app_title,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse
)


@app.middleware('http')
async def validate_ip(request: Request, call_next):
    ip = str(request.client.host)
    logger.info(f'request_ip: {ip}')
    if ip in BLOCKED_IPS:
        data = {
            'message': f'IP {ip} is not allowed to access this resource.'
        }
        return ORJSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=data)
    return await call_next(request)

app.include_router(base.router, prefix='/api')
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
