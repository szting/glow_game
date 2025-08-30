from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from typing import List, Dict
from translations import get_text

def get_mode_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Get mode selection keyboard"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text=get_text(lang, 'individual_mode'), callback_data='mode:individual'),
        InlineKeyboardButton(text=get_text(lang, 'couple_mode'), callback_data='mode:couple'),
        InlineKeyboardButton(text=get_text(lang, 'group_mode'), callback_data='mode:group')
    )
    return builder.as_markup()

def get_language_keyboard() -> InlineKeyboardMarkup:
    """Get language selection keyboard"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='English', callback_data='lang:en'),
        InlineKeyboardButton(text='中文', callback_data='lang:zh')
    )
    return builder.as_markup()

def get_challenge_keyboard(lang: str, challenge_id: str) -> InlineKeyboardMarkup:
    """Get challenge response keyboard"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text=get_text(lang, 'btn_complete'), callback_data=f'complete:{challenge_id}'),
        InlineKeyboardButton(text=get_text(lang, 'btn_skip'), callback_data=f'skip:{challenge_id}')
    )
    builder.row(
        InlineKeyboardButton(text=get_text(lang, 'btn_save'), callback_data=f'save:{challenge_id}')
    )
    return builder.as_markup()

def get_session_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Get session management keyboard"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text=get_text(lang, 'btn_new'), callback_data='session:new'),
        InlineKeyboardButton(text=get_text(lang, 'btn_save'), callback_data='session:save')
    )
    return builder.as_markup()

def get_settings_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Get settings menu keyboard"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text=get_text(lang, 'change_language'), callback_data='settings:language')
    )
    builder.row(
        InlineKeyboardButton(text=get_text(lang, 'change_mode'), callback_data='settings:mode')
    )
    builder.row(
        InlineKeyboardButton(text=get_text(lang, 'change_timezone'), callback_data='settings:timezone')
    )
    builder.row(
        InlineKeyboardButton(text=get_text(lang, 'btn_back'), callback_data='settings:back')
    )
    return builder.as_markup()

def get_couple_keyboard(lang: str, in_couple: bool = False) -> InlineKeyboardMarkup:
    """Get couple mode keyboard"""
    builder = InlineKeyboardBuilder()
    if not in_couple:
        builder.row(
            InlineKeyboardButton(text='Create Room', callback_data='couple:create'),
            InlineKeyboardButton(text='Join Room', callback_data='couple:join')
        )
    else:
        builder.row(
            InlineKeyboardButton(text='Leave Couple Mode', callback_data='couple:leave'),
            InlineKeyboardButton(text='View Partner Progress', callback_data='couple:partner')
        )
    return builder.as_markup()

def get_main_menu_keyboard(lang: str) -> ReplyKeyboardMarkup:
    """Get main menu keyboard"""
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text='🌈 Challenge'),
        KeyboardButton(text='📊 Progress')
    )
    builder.row(
        KeyboardButton(text='🔥 Streak'),
        KeyboardButton(text='🏆 Badges')
    )
    builder.row(
        KeyboardButton(text='⚙️ Settings'),
        KeyboardButton(text='❓ Help')
    )
    return builder.as_markup(resize_keyboard=True)
