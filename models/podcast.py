from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Podcast(Base):
    __tablename__ = "podcasts"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    language = Column(String, nullable=False)
    category = Column(String, nullable=False)
    rss_url = Column(String)
    cover_url = Column(String)
    created_at = Column(DateTime, server_default=func.now())