from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Episode(Base):
    __tablename__ = "episodes"

    id = Column(Integer, primary_key=True)
    podcast_id = Column(Integer, ForeignKey("podcasts.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    file_key = Column(String, nullable=False)
    publish_date = Column(Date)
    duration = Column(Integer)