from sqlalchemy import Column, String, Integer, Text, JSON, Boolean
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin, IDMixin

class Challenge(Base, IDMixin, TimestampMixin):
    __tablename__ = 'challenges'
    
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    color = Column(String(20), nullable=False, index=True)
    language = Column(String(10), default='en', nullable=False, index=True)
    is_active = Column(Boolean, default=True)
    
    # JSON field for additional metadata
    metadata = Column(JSON, default=dict)
    
    # Relationships
    responses = relationship("Response", back_populates="challenge")
    
    def __repr__(self):
        return f"<Challenge(title='{self.title}', color='{self.color}', language='{self.language}')>"
