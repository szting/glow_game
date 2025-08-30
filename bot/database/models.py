# Import all models to ensure they are registered with SQLAlchemy
from ..models import (
    User, Couple, Group, Challenge, Response, Session, ChallengeSuggestion
)

__all__ = [
    'User', 'Couple', 'Group', 'Challenge', 
    'Response', 'Session', 'ChallengeSuggestion'
]
