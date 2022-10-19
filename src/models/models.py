from datetime import datetime

from fastapi import Depends
from fastapi_users_db_sqlalchemy import (
    SQLAlchemyBaseUserTableUUID,
    SQLAlchemyUserDatabase
)
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String

from db.db import AsyncSession, Base, get_session


class URL(Base):
    __tablename__ = 'urls'
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    private = Column(Boolean)
    original_url = Column(String)
    short_url = Column(String)
    usage_count = Column(Integer)
    created_at = Column(DateTime, index=True, default=datetime.utcnow)
    owner = Column(ForeignKey('user.username'))


class User(SQLAlchemyBaseUserTableUUID, Base):
    username = Column(String, unique=True)
    urls = Column(ForeignKey('urls.id', ondelete='CASCADE'))


async def get_user_db(session: AsyncSession = Depends(get_session)):
    yield SQLAlchemyUserDatabase(session, User)
