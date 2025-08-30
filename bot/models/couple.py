from sqlalchemy import Column, String, Integer, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin, IDMixin

class Couple(Base, IDMixin, TimestampMixin):
    __tablename__ = 'couples'
    
    user1_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user2_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    room_code = Column(String(10), unique=True, nullable=False, index=True)
    joint_streak = Column(Integer, default=0)
    
    # JSON field for PostgreSQL compatibility
    joint_rainbow = Column(JSON, default=lambda: {
        'red': False, 'orange': False, 'yellow': False, 
        'green': False, 'blue': False, 'indigo': False, 'violet': False
    })
    
    # Relationships
    user1 = relationship("User", foreign_keys=[user1_id])
    user2 = relationship("User", foreign_keys=[user2_id])
    responses = relationship("Response", back_populates="couple")
    
    def __repr__(self):
        return f"<Couple(room_code='{self.room_code}', users={self.user1_id},{self.user2_id})>"
