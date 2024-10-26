from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class Posts(Base):
    __tablename__: str = "posts"
    
    id: int = Column(Integer, primary_key=True, index=True)
    title: str = Column(String, index=True)
    content: str = Column(String)
    created_at: DateTime = Column(DateTime(timezone=True), server_default=func.now())
    updated_at: DateTime = Column(DateTime(timezone=True), onupdate=func.now())
