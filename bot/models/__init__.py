# Import all models safely
__all__ = [
    'User',
    'Couple', 
    'Group',
    'Challenge',
    'Response',
    'Session',
    'ChallengeSuggestion'
]

# Import models only when needed to avoid startup errors
def get_models():
    """Get all models when needed"""
    try:
        from .user import User
        from .couple import Couple
        from .group import Group
        from .challenge import Challenge
        from .response import Response
        from .session import Session
        from .suggestion import ChallengeSuggestion
        
        return {
            'User': User,
            'Couple': Couple,
            'Group': Group,
            'Challenge': Challenge,
            'Response': Response,
            'Session': Session,
            'ChallengeSuggestion': ChallengeSuggestion
        }
    except ImportError as e:
        print(f"Warning: Could not import models: {e}")
        return {}