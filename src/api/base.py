from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import ORJSONResponse, RedirectResponse
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session
from models.models import User
from schemas import urls
from services.urls import urls_crud
from users.manager import current_active_user

router = APIRouter()


@router.get('/user/{user_username}', response_model=list[urls.URL])
async def get_user_urls(
        db: AsyncSession = Depends(get_session),
        user_username: str = None
) -> any:
    user_urls_list = await urls_crud.get_user_urls(db=db, username=user_username)
    return user_urls_list


@router.get('/urls', response_model=list[urls.URL])
async def get_all_urls(
        db: AsyncSession = Depends(get_session),
        skip: int = 0,
        limit: int = 100,
) -> any:
    urls_list = await urls_crud.get_multi(db=db, skip=skip, limit=limit)
    return urls_list


@router.get('/urls/{url_id}')
async def get_url(
        *,
        db: AsyncSession = Depends(get_session),
        url_id: int,
) -> any:
    url = await urls_crud.get(db=db, url_id=url_id)
    if not url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return RedirectResponse(url)


@router.get('/urls/{url_id}/status')
async def get_status(
        *,
        db: AsyncSession = Depends(get_session),
        url_id: int,
) -> any:
    url_status = await urls_crud.get_status(db=db, url_id=url_id)
    if not status:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return ORJSONResponse(url_status)


@router.post('/urls', status_code=status.HTTP_201_CREATED)
async def create_url(
        *,
        db: AsyncSession = Depends(get_session),
        url_in: urls.URLCreate,
        user: Optional[User] = Depends(current_active_user),
) -> any:
    logger.info(f'User: {user.email}')
    url = await urls_crud.create(db=db, obj_in=url_in, user=user)
    return url
