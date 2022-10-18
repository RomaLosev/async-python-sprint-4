from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel


class URLBase(BaseModel):
    title: str
    original_url: str


class URLCreate(URLBase):
    pass


class URLInDBBase(URLBase):
    id: int
    title: Union[str, None] = None
    original_url: Union[str, None] = None
    private: bool = False
    short_url: Union[str, None] = None
    usage_count: int = 0
    created_at: datetime = None
    owner: Optional[str] = None

    class Config:
        orm_mode = True


class URL(URLInDBBase):
    pass


class URLInDB(URLInDBBase):
    pass
