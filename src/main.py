from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse
from core.config import app_settings
from api import base
from loguru import logger

app = FastAPI(
    title=app_settings.app_title,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse
)

BLOCKED_IPS = []


@app.middleware('http')
async def validate_ip(request: Request, call_next):
    ip = str(request.client.host)
    logger.info(f'request_ip: {ip}')
    if ip in BLOCKED_IPS:
        data = {
            'message': f'IP {ip} is not allowed to access this resource.'
        }
        return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=data)
    return await call_next(request)

app.include_router(base.router, prefix='/api')
