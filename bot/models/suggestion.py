from sqlalchemy import Column, String, Integer, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin, IDMixin

class ChallengeSuggestion(Base, IDMixin, TimestampMixin):
    __tablename__ = 'challenge_suggestions'
    
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    color = Column(String(20), nullable=False)
    language = Column(String(10), default='en', nullable=False)
    status = Column(String(20), default='pending')  # pending, approved, rejected
    
    # JSON field for additional metadata
    metadata = Column(JSON, default=dict)
    
    # Relationships
    user = relationship("User", back_populates="suggestions")
    
    def __repr__(self):
        return f"<ChallengeSuggestion(title='{self.title}', color='{self.color}', status='{self.status}')>"
