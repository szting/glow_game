from sqlalchemy import Column, String, Integer, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin, IDMixin

class Response(Base, IDMixin, TimestampMixin):
    __tablename__ = 'responses'
    
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    challenge_id = Column(Integer, ForeignKey('challenges.id'), nullable=False)
    response_type = Column(String(20), default='text')  # text, photo, voice, video
    response_content = Column(Text, nullable=False)
    mode = Column(String(20), default='individual')  # individual, couple, group
    
    # Optional foreign keys for couple/group modes
    couple_id = Column(Integer, ForeignKey('couples.id'), nullable=True)
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=True)
    
    # JSON field for additional response data
    metadata = Column(JSON, default=dict)
    
    # Relationships
    user = relationship("User", back_populates="responses")
    challenge = relationship("Challenge", back_populates="responses")
    couple = relationship("Couple", back_populates="responses")
    group = relationship("Group", back_populates="responses")
    
    def __repr__(self):
        return f"<Response(user_id={self.user_id}, challenge_id={self.challenge_id}, type='{self.response_type}')>"
