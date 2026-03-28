from sqlalchemy import Column, String, Text, Boolean, DateTime, JSON, func
from datetime import datetime
from app.db.base import Base


class Algorithm(Base):
    """Algorithm metadata and parameter definitions"""
    __tablename__ = "algorithms"
    
    id = Column(String(50), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    version = Column(String(20), default="1.0")
    is_active = Column(Boolean, default=True)
    parameters = Column(JSON, nullable=False)  # JSON array of parameter definitions
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Algorithm {self.id}>"
