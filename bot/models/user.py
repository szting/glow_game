from sqlalchemy import Column, String, Integer, Text, JSON, Boolean
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin, IDMixin

class User(Base, IDMixin, TimestampMixin):
    __tablename__ = 'users'
    
    telegram_id = Column(Integer, unique=True, nullable=False, index=True)
    username = Column(String(100), nullable=True)
    language = Column(String(10), default='en', nullable=False)
    mode = Column(String(20), default='individual', nullable=False)
    timezone = Column(String(50), default='UTC', nullable=False)
    
    # JSON fields for PostgreSQL compatibility
    rainbow_progress = Column(JSON, default=lambda: {
        'red': False, 'orange': False, 'yellow': False, 
        'green': False, 'blue': False, 'indigo': False, 'violet': False
    })
    points = Column(JSON, default=lambda: {
        'spark': 0, 'cozy': 0, 'sunshine': 0, 'zen': 0, 
        'anchor': 0, 'sage': 0, 'enigma': 0
    })
    badges = Column(JSON, default=list)
    streak = Column(Integer, default=0)
    total_challenges = Column(Integer, default=0)
    last_activity = Column(String(50), nullable=True)  # Store as ISO string for compatibility
    
    # Relationships
    responses = relationship("Response", back_populates="user")
    sessions = relationship("Session", back_populates="user")
    suggestions = relationship("ChallengeSuggestion", back_populates="user")
    
    def __repr__(self):
        return f"<User(telegram_id={self.telegram_id}, username='{self.username}')>"
