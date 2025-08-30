import os
from typing import Dict, List, Optional
from pydantic import BaseSettings, Field
from pydantic_settings import BaseSettings as PydanticBaseSettings

class Settings(PydanticBaseSettings):
    """Application settings with environment variable support"""
    
    # Bot Configuration
    bot_token: str = Field(..., env='BOT_TOKEN')
    webhook_url: Optional[str] = Field(None, env='WEBHOOK_URL')
    webhook_secret: Optional[str] = Field(None, env='WEBHOOK_SECRET')
    
    # Database Configuration
    database_url: Optional[str] = Field(None, env='DATABASE_URL')
    
    # API Keys
    openai_api_key: Optional[str] = Field(None, env='OPENAI_API_KEY')
    giphy_api_key: Optional[str] = Field(None, env='GIPHY_API_KEY')
    
    # Application Settings
    debug: bool = Field(False, env='DEBUG')
    environment: str = Field('development', env='ENVIRONMENT')
    
    # Server Configuration
    host: str = Field('0.0.0.0', env='HOST')
    port: int = Field(8000, env='PORT')
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
_settings: Optional[Settings] = None

def get_settings() -> Settings:
    """Get application settings singleton"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings

# Rainbow Configuration
RAINBOW_COLORS = {
    'red': {'name': 'Red', 'emoji': '🔴', 'theme': 'Passion', 'points': 'spark'},
    'orange': {'name': 'Orange', 'emoji': '🟠', 'theme': 'Warmth', 'points': 'cozy'},
    'yellow': {'name': 'Yellow', 'emoji': '🟡', 'theme': 'Happiness', 'points': 'sunshine'},
    'green': {'name': 'Green', 'emoji': '🟢', 'theme': 'Peace', 'points': 'zen'},
    'blue': {'name': 'Blue', 'emoji': '🔵', 'theme': 'Trust', 'points': 'anchor'},
    'indigo': {'name': 'Indigo', 'emoji': '🟦', 'theme': 'Depth', 'points': 'sage'},
    'violet': {'name': 'Violet', 'emoji': '🟣', 'theme': 'Mystique', 'points': 'enigma'}
}

# Language Configuration
LANGUAGES = {
    'en': 'English',
    'zh': '中文'
}

# Achievement Badges
BADGES = {
    'rainbow_starter': {'name': 'Rainbow Starter', 'emoji': '🌈', 'requirement': 'Complete first challenge'},
    'peace_keeper': {'name': 'Peace Keeper', 'emoji': '🟢', 'requirement': 'Complete 5 green challenges'},
    'full_rainbow': {'name': 'Full Rainbow Achiever', 'emoji': '✨', 'requirement': 'Complete all 7 colors'},
    'streak_master': {'name': 'Streak Master', 'emoji': '🔥', 'requirement': '7 day streak'},
    'love_champion': {'name': 'Love Champion', 'emoji': '💖', 'requirement': '30 challenges completed'}
}

# Default Daily Schedule (in hours, 24-hour format)
DEFAULT_PROMPT_TIME = 9  # 9 AM local time
