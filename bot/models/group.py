from sqlalchemy import Column, String, Integer, Text, JSON
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin, IDMixin

class Group(Base, IDMixin, TimestampMixin):
    __tablename__ = 'groups'
    
    chat_id = Column(Integer, unique=True, nullable=False, index=True)
    title = Column(String(200), nullable=False)
    
    # JSON fields for PostgreSQL compatibility
    collective_rainbow = Column(JSON, default=lambda: {
        'red': False, 'orange': False, 'yellow': False, 
        'green': False, 'blue': False, 'indigo': False, 'violet': False
    })
    active_members = Column(JSON, default=list)
    
    # Relationships
    responses = relationship("Response", back_populates="group")
    
    def __repr__(self):
        return f"<Group(chat_id={self.chat_id}, title='{self.title}')>"
