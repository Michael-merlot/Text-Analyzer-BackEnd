from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from sqlalchemy.sql import func
from app.database.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    word_count = Column(Integer)
    sentence_count = Column(Integer)
    readability_score = Column(Float)
    keywords = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
