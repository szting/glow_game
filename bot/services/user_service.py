from typing import Optional, Dict, List
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime, timezone
import json

from ..models.user import User
from ..models.couple import Couple
from ..models.response import Response
from ..utils import calculate_streak, check_badge_eligibility

class UserService:
    def __init__(self, db: Session):
        self.db = db
    
    async def create_user(self, telegram_id: int, username: str, language: str = 'en', 
                          mode: str = 'individual', timezone: str = 'UTC') -> User:
        """Create a new user in the database"""
        user = User(
            telegram_id=telegram_id,
            username=username,
            language=language,
            mode=mode,
            timezone=timezone,
            rainbow_progress={
                'red': False, 'orange': False, 'yellow': False, 
                'green': False, 'blue': False, 'indigo': False, 'violet': False
            },
            points={
                'spark': 0, 'cozy': 0, 'sunshine': 0, 'zen': 0, 
                'anchor': 0, 'sage': 0, 'enigma': 0
            },
            badges=[],
            streak=0,
            total_challenges=0
        )
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    async def get_user(self, telegram_id: int) -> Optional[User]:
        """Get user by telegram ID"""
        return self.db.query(User).filter(User.telegram_id == telegram_id).first()
    
    async def update_user(self, telegram_id: int, updates: Dict) -> Optional[User]:
        """Update user information"""
        user = await self.get_user(telegram_id)
        if not user:
            return None
        
        for key, value in updates.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        self.db.commit()
        self.db.refresh(user)
        return user
    
    async def update_user_activity(self, telegram_id: int) -> Optional[User]:
        """Update user's last activity and recalculate streak"""
        user = await self.get_user(telegram_id)
        if not user:
            return None
        
        now = datetime.now(timezone.utc)
        user.last_activity = now.isoformat()
        
        # Recalculate streak
        if user.last_activity:
            last_activity = datetime.fromisoformat(user.last_activity.replace('Z', '+00:00'))
            user.streak = calculate_streak(last_activity, user.streak)
        
        self.db.commit()
        self.db.refresh(user)
        return user
    
    async def complete_challenge(self, telegram_id: int, challenge_color: str, 
                                points_earned: int) -> Optional[User]:
        """Mark a challenge as completed and update user progress"""
        user = await self.get_user(telegram_id)
        if not user:
            return None
        
        # Update rainbow progress
        if challenge_color in user.rainbow_progress:
            user.rainbow_progress[challenge_color] = True
        
        # Update points
        point_type = self._get_point_type_for_color(challenge_color)
        if point_type in user.points:
            user.points[point_type] += points_earned
        
        # Update total challenges
        user.total_challenges += 1
        
        # Check for new badges
        new_badges = check_badge_eligibility({
            'total_challenges': user.total_challenges,
            'points': user.points,
            'rainbow_progress': user.rainbow_progress,
            'streak': user.streak
        })
        
        for badge in new_badges:
            if badge not in user.badges:
                user.badges.append(badge)
        
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def _get_point_type_for_color(self, color: str) -> str:
        """Get the point type associated with a color"""
        color_points = {
            'red': 'spark',
            'orange': 'cozy', 
            'yellow': 'sunshine',
            'green': 'zen',
            'blue': 'anchor',
            'indigo': 'sage',
            'violet': 'enigma'
        }
        return color_points.get(color, 'spark')
    
    async def get_user_stats(self, telegram_id: int) -> Optional[Dict]:
        """Get comprehensive user statistics"""
        user = await self.get_user(telegram_id)
        if not user:
            return None
        
        # Get recent responses
        recent_responses = self.db.query(Response).filter(
            Response.user_id == user.id
        ).order_by(Response.created_at.desc()).limit(10).all()
        
        return {
            'user': user,
            'recent_responses': recent_responses,
            'rainbow_completion': sum(user.rainbow_progress.values()),
            'total_points': sum(user.points.values())
        }
