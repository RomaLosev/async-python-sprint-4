from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from db.db import Base


class URL(Base):
    __tablename__ = 'urls'
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    original_url = Column(String)
    short_url = Column(String)
    usage_count = Column(Integer)
    created_at = Column(DateTime, index=True, default=datetime.utcnow)
