from supabase import create_client, Client
from datetime import datetime, timezone
from typing import Optional, Dict, List, Any
import json
from config import SUPABASE_URL, SUPABASE_KEY

class Database:
    def __init__(self):
        self.client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # User Management
    async def create_user(self, telegram_id: int, username: str, language: str = 'en', 
                          mode: str = 'individual', timezone: str = 'UTC') -> Dict:
        """Create a new user in the database"""
        data = {
            'telegram_id': telegram_id,
            'username': username,
            'language': language,
            'mode': mode,
            'timezone': timezone,
            'created_at': datetime.now(timezone.utc).isoformat(),
            'rainbow_progress': json.dumps({color: False for color in ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']}),
            'points': json.dumps({'spark': 0, 'cozy': 0, 'sunshine': 0, 'zen': 0, 'anchor': 0, 'sage': 0, 'enigma': 0}),
            'streak': 0,
            'badges': json.dumps([])
        }
        
        result = self.client.table('users').insert(data).execute()
        return result.data[0] if result.data else None
    
    async def get_user(self, telegram_id: int) -> Optional[Dict]:
        """Get user by telegram ID"""
        result = self.client.table('users').select('*').eq('telegram_id', telegram_id).execute()
        if result.data:
            user = result.data[0]
            user['rainbow_progress'] = json.loads(user['rainbow_progress'])
            user['points'] = json.loads(user['points'])
            user['badges'] = json.loads(user['badges'])
            return user
        return None
    
    async def update_user(self, telegram_id: int, updates: Dict) -> Dict:
        """Update user information"""
        # Convert complex types to JSON strings
        if 'rainbow_progress' in updates and isinstance(updates['rainbow_progress'], dict):
            updates['rainbow_progress'] = json.dumps(updates['rainbow_progress'])
        if 'points' in updates and isinstance(updates['points'], dict):
            updates['points'] = json.dumps(updates['points'])
        if 'badges' in updates and isinstance(updates['badges'], list):
            updates['badges'] = json.dumps(updates['badges'])
        
        result = self.client.table('users').update(updates).eq('telegram_id', telegram_id).execute()
        return result.data[0] if result.data else None
    
    # Couple Management
    async def create_couple(self, user1_id: int, user2_id: int, room_code: str) -> Dict:
        """Create a couple connection"""
        data = {
            'user1_id': user1_id,
            'user2_id': user2_id,
            'room_code': room_code,
            'created_at': datetime.now(timezone.utc).isoformat(),
            'joint_streak': 0,
            'joint_rainbow': json.dumps({color: False for color in ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']})
        }
        
        result = self.client.table('couples').insert(data).execute()
        return result.data[0] if result.data else None
    
    async def get_couple_by_user(self, telegram_id: int) -> Optional[Dict]:
        """Get couple information by user ID"""
        result = self.client.table('couples').select('*').or_(f'user1_id.eq.{telegram_id},user2_id.eq.{telegram_id}').execute()
        if result.data:
            couple = result.data[0]
            couple['joint_rainbow'] = json.loads(couple['joint_rainbow'])
            return couple
        return None
    
    async def get_couple_by_room(self, room_code: str) -> Optional[Dict]:
        """Get couple by room code"""
        result = self.client.table('couples').select('*').eq('room_code', room_code).execute()
        if result.data:
            couple = result.data[0]
            couple['joint_rainbow'] = json.loads(couple['joint_rainbow'])
            return couple
        return None
    
    # Group Management
    async def create_group(self, chat_id: int, title: str) -> Dict:
        """Create a group entry"""
        data = {
            'chat_id': chat_id,
            'title': title,
            'created_at': datetime.now(timezone.utc).isoformat(),
            'collective_rainbow': json.dumps({color: False for color in ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']}),
            'active_members': json.dumps([])
        }
        
        result = self.client.table('groups').insert(data).execute()
        return result.data[0] if result.data else None
    
    async def get_group(self, chat_id: int) -> Optional[Dict]:
        """Get group by chat ID"""
        result = self.client.table('groups').select('*').eq('chat_id', chat_id).execute()
        if result.data:
            group = result.data[0]
            group['collective_rainbow'] = json.loads(group['collective_rainbow'])
            group['active_members'] = json.loads(group['active_members'])
            return group
        return None
    
    async def update_group(self, chat_id: int, updates: Dict) -> Dict:
        """Update group information"""
        if 'collective_rainbow' in updates and isinstance(updates['collective_rainbow'], dict):
            updates['collective_rainbow'] = json.dumps(updates['collective_rainbow'])
        if 'active_members' in updates and isinstance(updates['active_members'], list):
            updates['active_members'] = json.dumps(updates['active_members'])
        
        result = self.client.table('groups').update(updates).eq('chat_id', chat_id).execute()
        return result.data[0] if result.data else None
    
    # Challenge Management
    async def get_challenges(self, color: str = None, language: str = 'en') -> List[Dict]:
        """Get challenges, optionally filtered by color"""
        query = self.client.table('challenges').select('*').eq('language', language)
        if color:
            query = query.eq('color', color)
        
        result = query.execute()
        return result.data if result.data else []
    
    async def create_challenge(self, challenge_data: Dict) -> Dict:
        """Create a new challenge"""
        result = self.client.table('challenges').insert(challenge_data).execute()
        return result.data[0] if result.data else None
    
    async def suggest_challenge(self, user_id: int, suggestion: Dict) -> Dict:
        """Save a user's challenge suggestion"""
        data = {
            'user_id': user_id,
            'suggestion': json.dumps(suggestion),
            'created_at': datetime.now(timezone.utc).isoformat(),
            'status': 'pending'
        }
        
        result = self.client.table('challenge_suggestions').insert(data).execute()
        return result.data[0] if result.data else None
    
    # Response Management
    async def save_response(self, user_id: int, challenge_id: str, response_data: Dict) -> Dict:
        """Save user's response to a challenge"""
        data = {
            'user_id': user_id,
            'challenge_id': challenge_id,
            'response_type': response_data.get('type', 'text'),
            'response_content': response_data.get('content', ''),
            'created_at': datetime.now(timezone.utc).isoformat(),
            'mode': response_data.get('mode', 'individual'),
            'couple_id': response_data.get('couple_id'),
            'group_id': response_data.get('group_id')
        }
        
        result = self.client.table('responses').insert(data).execute()
        return result.data[0] if result.data else None
    
    async def get_user_responses(self, user_id: int, limit: int = 10) -> List[Dict]:
        """Get user's recent responses"""
        result = self.client.table('responses').select('*').eq('user_id', user_id).order('created_at', desc=True).limit(limit).execute()
        return result.data if result.data else []
    
    # Session Management
    async def save_session(self, user_id: int, session_data: Dict) -> Dict:
        """Save incomplete challenge session"""
        data = {
            'user_id': user_id,
            'session_data': json.dumps(session_data),
            'created_at': datetime.now(timezone.utc).isoformat(),
            'expires_at': session_data.get('expires_at')
        }
        
        result = self.client.table('sessions').insert(data).execute()
        return result.data[0] if result.data else None
    
    async def get_active_session(self, user_id: int) -> Optional[Dict]:
        """Get user's active session"""
        result = self.client.table('sessions').select('*').eq('user_id', user_id).gt('expires_at', datetime.now(timezone.utc).isoformat()).order('created_at', desc=True).limit(1).execute()
        if result.data:
            session = result.data[0]
            session['session_data'] = json.loads(session['session_data'])
            return session
        return None
    
    async def delete_session(self, session_id: str) -> bool:
        """Delete a session"""
        result = self.client.table('sessions').delete().eq('id', session_id).execute()
        return True
    
    # Real-time subscriptions for couple mode
    def subscribe_to_couple_responses(self, couple_id: str, callback):
        """Subscribe to real-time updates for couple responses"""
        channel = self.client.channel(f'couple_{couple_id}')
        channel.on_postgres_changes(
            event='INSERT',
            schema='public',
            table='responses',
            filter=f'couple_id=eq.{couple_id}'
        ).subscribe(callback)
        return channel
