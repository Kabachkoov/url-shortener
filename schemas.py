from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional


class URLBase(BaseModel):
    original_url: HttpUrl


class URLCreate(URLBase):
    custom_code: Optional[str] = None


class URLUpdate(BaseModel):
    is_active: Optional[bool] = None


class URLInDB(URLBase):
    id: int
    short_code: str
    user_id: Optional[int]
    clicks: int
    created_at: datetime
    last_accessed: Optional[datetime]
    is_active: bool
    
    class Config:
        from_attributes = True


class URL(URLInDB):
    short_url: str


class URLAnalytics(URL):
    pass
