from sqlalchemy import Column, Integer, Text, TIMESTAMP
from sqlalchemy.sql import func
from database import Base

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

