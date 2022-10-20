from abc import ABC, abstractmethod
from typing import Generic, Optional, Type, TypeVar

import pyshorteners
from fastapi.encoders import jsonable_encoder
from loguru import logger
from pydantic import BaseModel
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)


class Repository(ABC):

    @abstractmethod
    def get(self, *args, **kwargs):
        pass

    @abstractmethod
    def create(self, *args, **kwargs):
        raise NotImplementedError


class RepositoryDB(Repository, Generic[ModelType, CreateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self._model = model

    async def update_counter(self, db: AsyncSession, url_id: int, counter: int):
        """
        Update usage_counter in db
        """
        statement = (
            update(self._model)
            .filter_by(id=url_id)
            .values(usage_count=counter+1)
        )
        await db.execute(statement=statement)
        await db.commit()

    async def get_item(self, db: AsyncSession, url_id: int):
        """
        Get obj from DB by id
        """
        statement = select(self._model).where(self._model.id == url_id)
        obj = await db.scalar(statement=statement)
        return obj

    async def get_user_urls(
             self,
            db: AsyncSession,
            username: str
    ) -> Optional[ModelType]:
        statement = select(self._model).where(self._model.owner.username == username)
        urls = await db.scalars(statement=statement)
        return urls

    async def get(
            self,
            db: AsyncSession,
            url_id: int
    ) -> Optional[ModelType]:
        url = await self.get_item(db, url_id)
        result = url.original_url
        counter = url.usage_count
        await self.update_counter(db, url_id, counter)
        if result.startswith(('https://', 'http://')):
            return result
        else:
            return f'https://{result}'

    async def get_status(
            self, db: AsyncSession,
            url_id: int,
    ) -> Optional[ModelType]:
        url = await self.get_item(db, url_id)
        if not url.private:
            return url.usage_count

    @staticmethod
    def shortener(url: str) -> str:
        shortener = pyshorteners.Shortener()
        short_url = shortener.tinyurl.short(url)
        return short_url

    async def create(
            self, db: AsyncSession,
            *, obj_in: CreateSchemaType,
            user: ModelType
    ) -> ModelType:
        logger.info(f'obj_in: {obj_in}')
        obj_in_data = jsonable_encoder(obj_in)
        logger.info(f'obj_in_data: {obj_in_data}')
        db_obj = self._model(**obj_in_data)
        db_obj.short_url = self.shortener(db_obj.original_url)
        if user:
            db_obj.owner = user.username
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
