from datetime import datetime

from pydantic import BaseModel


class URLBase(BaseModel):
    title: str
    original_url: str


class URLCreate(URLBase):
    pass


class URLInDBBase(URLBase):
    id: int
    title: str | None
    original_url: str | None
    private: bool = False
    short_url: str | None
    usage_count: int = 0
    created_at: datetime | None
    owner: str | None

    class Config:
        orm_mode = True


class URL(URLInDBBase):
    pass


class URLInDB(URLInDBBase):
    pass
