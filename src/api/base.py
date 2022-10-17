from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.responses import RedirectResponse, ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger
from db.db import get_session
from schemas import urls
from services.urls import urls_crud

router = APIRouter()


@router.get('/urls', response_model=list[urls.URL])
async def get_all_urls(
        db: AsyncSession = Depends(get_session),
        skip: int = 0,
        limit: int = 100,
) -> any:
    urls_list = await urls_crud.get_multi(db=db, skip=skip, limit=limit)
    logger.info(urls_list)
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
) -> any:
    url = await urls_crud.create(db=db, obj_in=url_in)
    return url
