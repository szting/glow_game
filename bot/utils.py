import random
import string
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import pytz
from PIL import Image, ImageDraw, ImageFont
import io
import aiohttp
import openai
from config import OPENAI_API_KEY, GIPHY_API_KEY, RAINBOW_COLORS

def generate_room_code() -> str:
    """Generate a unique room code for couple mode"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def get_rainbow_progress_bar(progress: Dict[str, bool]) -> str:
    """Generate visual rainbow progress bar"""
    bar = ""
    for color in ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']:
        if progress.get(color, False):
            bar += RAINBOW_COLORS[color]['emoji']
        else:
            bar += '⚪'
    return bar

def calculate_streak(last_activity: datetime, current_streak: int) -> int:
    """Calculate user's streak based on last activity"""
    if not last_activity:
        return 0
    
    now = datetime.now(pytz.UTC)
    last_activity = last_activity.replace(tzinfo=pytz.UTC) if last_activity.tzinfo is None else last_activity
    
    time_diff = now - last_activity
    
    if time_diff.days == 0:
        return current_streak
    elif time_diff.days == 1:
        return current_streak + 1
    else:
        return 0

def get_next_color(progress: Dict[str, bool]) -> Optional[str]:
    """Get the next color in the rainbow sequence"""
    colors = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']
    for color in colors:
        if not progress.get(color, False):
            return color
    return colors[0]  # Start over if all complete

def format_datetime_local(dt: datetime, timezone_str: str) -> str:
    """Format datetime to user's local timezone"""
    tz = pytz.timezone(timezone_str)
    local_dt = dt.astimezone(tz)
    return local_dt.strftime('%Y-%m-%d %H:%M')

async def generate_achievement_card(user_name: str, achievement: str, rainbow_progress: Dict) -> bytes:
    """Generate an achievement card image"""
    # Create image
    width, height = 800, 400
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw gradient background
    for i in range(height):
        color_value = int(255 - (i / height) * 50)
        draw.rectangle([(0, i), (width, i+1)], fill=(color_value, color_value, 255))
    
    # Draw rainbow progress
    x_start = 100
    y_pos = 250
    circle_size = 40
    spacing = 90
    
    colors_rgb = {
        'red': (255, 0, 0),
        'orange': (255, 165, 0),
        'yellow': (255, 255, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255),
        'indigo': (75, 0, 130),
        'violet': (238, 130, 238)
    }
    
    for i, color in enumerate(['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']):
        x_pos = x_start + (i * spacing)
        if rainbow_progress.get(color, False):
            draw.ellipse([(x_pos, y_pos), (x_pos + circle_size, y_pos + circle_size)], 
                        fill=colors_rgb[color])
        else:
            draw.ellipse([(x_pos, y_pos), (x_pos + circle_size, y_pos + circle_size)], 
                        fill=(200, 200, 200))
    
    # Add text (using default font)
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
        font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
    
    # Draw achievement text
    draw.text((width//2, 100), achievement, fill='white', font=font_large, anchor='mm')
    draw.text((width//2, 160), f"Congratulations, {user_name}!", fill='white', font=font_medium, anchor='mm')
    
    # Convert to bytes
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    return img_byte_arr.getvalue()

async def get_random_gif(search_term: str) -> Optional[str]:
    """Get a random GIF from Giphy"""
    if not GIPHY_API_KEY:
        return None
    
    url = f"https://api.giphy.com/v1/gifs/random"
    params = {
        'api_key': GIPHY_API_KEY,
        'tag': search_term,
        'rating': 'g'
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                return data['data']['images']['original']['url']
    
    return None

async def generate_challenge_image(challenge: Dict) -> Optional[bytes]:
    """Generate an image for a challenge using OpenAI DALL-E"""
    if not OPENAI_API_KEY:
        return None
    
    openai.api_key = OPENAI_API_KEY
    
    try:
        response = openai.Image.create(
            prompt=f"A warm, romantic illustration for a relationship challenge: {challenge['title']}. Style: soft watercolor, peaceful, loving atmosphere",
            n=1,
            size="512x512"
        )
        
        image_url = response['data'][0]['url']
        
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as resp:
                if resp.status == 200:
                    return await resp.read()
    except Exception as e:
        print(f"Error generating image: {e}")
    
    return None

def check_badge_eligibility(user_data: Dict) -> List[str]:
    """Check which badges user is eligible for"""
    new_badges = []
    current_badges = user_data.get('badges', [])
    
    # Rainbow Starter - First challenge completed
    if user_data.get('total_challenges', 0) >= 1 and 'rainbow_starter' not in current_badges:
        new_badges.append('rainbow_starter')
    
    # Peace Keeper - 5 green challenges
    if user_data.get('points', {}).get('zen', 0) >= 50 and 'peace_keeper' not in current_badges:
        new_badges.append('peace_keeper')
    
    # Full Rainbow - All 7 colors completed
    rainbow = user_data.get('rainbow_progress', {})
    if all(rainbow.get(color, False) for color in ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']) and 'full_rainbow' not in current_badges:
        new_badges.append('full_rainbow')
    
    # Streak Master - 7 day streak
    if user_data.get('streak', 0) >= 7 and 'streak_master' not in current_badges:
        new_badges.append('streak_master')
    
    # Love Champion - 30 challenges completed
    if user_data.get('total_challenges', 0) >= 30 and 'love_champion' not in current_badges:
        new_badges.append('love_champion')
    
    return new_badges

def get_timezone_keyboard() -> InlineKeyboardMarkup:
    """Get timezone selection keyboard"""
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    
    builder = InlineKeyboardBuilder()
    
    common_timezones = [
        ('UTC', 'UTC'),
        ('US/Eastern', 'Eastern Time'),
        ('US/Central', 'Central Time'),
        ('US/Mountain', 'Mountain Time'),
        ('US/Pacific', 'Pacific Time'),
        ('Europe/London', 'London'),
        ('Europe/Paris', 'Paris'),
        ('Asia/Shanghai', 'Shanghai'),
        ('Asia/Tokyo', 'Tokyo'),
        ('Australia/Sydney', 'Sydney')
    ]
    
    for tz_code, tz_name in common_timezones:
        builder.row(InlineKeyboardButton(text=tz_name, callback_data=f'tz:{tz_code}'))
    
    return builder.as_markup()
