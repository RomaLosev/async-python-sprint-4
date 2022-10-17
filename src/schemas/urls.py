from typing import Union, Optional
from datetime import datetime

from pydantic import BaseModel


class URLBase(BaseModel):
    title: str
    original_url: str


class URLCreate(URLBase):
    usage_count: int = 0


class URLInDBBase(URLBase):
    id: int
    title: Union[str, None] = None
    original_url: Union[str, None] = None
    short_url: Union[str, None] = None
    usage_count: Optional[int] = 0
    created_at: datetime = None

    class Config:
        orm_mode = True


class URL(URLInDBBase):
    pass


class URLInDB(URLInDBBase):
    pass
