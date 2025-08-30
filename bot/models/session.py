from sqlalchemy import Column, String, Integer, Text, JSON, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin, IDMixin

class Session(Base, IDMixin, TimestampMixin):
    __tablename__ = 'sessions'
    
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    session_data = Column(JSON, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="sessions")
    
    def __repr__(self):
        return f"<Session(user_id={self.user_id}, expires_at={self.expires_at})>"
