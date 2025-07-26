from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List, Dict, Any

def main_menu_keyboard() -> InlineKeyboardMarkup:
    """Main menu keyboard for users"""
    keyboard = [
        [InlineKeyboardButton(text="🔍 Найти фильм/аниме/дораму по коду", callback_data="search_content")],
        [InlineKeyboardButton(text="👥 Партнёры", callback_data="show_partners")],
        [InlineKeyboardButton(text="ℹ️ Помощь", callback_data="show_help")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def subscription_check_keyboard() -> InlineKeyboardMarkup:
    """Keyboard for subscription verification"""
    keyboard = [
        [InlineKeyboardButton(text="✅ Проверить подписку", callback_data="check_subscription")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def partners_subscription_keyboard(partners: List[str]) -> InlineKeyboardMarkup:
    """Create keyboard with partner links for subscription"""
    keyboard = []
    
    for i, partner in enumerate(partners, 1):
        # Clean partner name for display
        display_name = partner.replace("@", "")
        keyboard.append([
            InlineKeyboardButton(
                text=f"Партнёр {i}", 
                url=f"https://t.me/{display_name}"
            )
        ])
    
    keyboard.append([InlineKeyboardButton(text="✅ Проверить подписку", callback_data="check_subscription")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def back_to_menu_keyboard() -> InlineKeyboardMarkup:
    """Back to menu keyboard"""
    keyboard = [
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def admin_menu_keyboard() -> InlineKeyboardMarkup:
    """Admin menu keyboard"""
    keyboard = [
        [InlineKeyboardButton(text="➕ Добавить запись", callback_data="admin_add_movie")],
        [InlineKeyboardButton(text="❌ Удалить запись", callback_data="admin_delete_movie")],
        [InlineKeyboardButton(text="🤝 Управление партнёрами", callback_data="admin_manage_partners")],
        [InlineKeyboardButton(text="📊 Статистика", callback_data="admin_statistics")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def partners_management_keyboard(partners: List[str]) -> InlineKeyboardMarkup:
    """Partners management keyboard"""
    keyboard = []
    
    # Add delete buttons for each partner
    for partner in partners:
        keyboard.append([
            InlineKeyboardButton(
                text=f"❌ {partner}", 
                callback_data=f"delete_partner:{partner}"
            )
        ])
    
    # Add new partner button
    keyboard.append([InlineKeyboardButton(text="➕ Добавить партнёра", callback_data="add_partner")])
    keyboard.append([InlineKeyboardButton(text="🔙 Назад", callback_data="admin_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def movie_episodes_keyboard(episodes: List[str]) -> InlineKeyboardMarkup:
    """Create keyboard with episode buttons"""
    keyboard = []
    
    for i, episode_url in enumerate(episodes, 1):
        keyboard.append([
            InlineKeyboardButton(
                text=f"▶ Эпизод {i}", 
                url=episode_url
            )
        ])
    
    keyboard.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def partners_list_keyboard(partners: List[str]) -> InlineKeyboardMarkup:
    """Create keyboard with partner links"""
    keyboard = []
    
    for i, partner in enumerate(partners, 1):
        # Clean partner name for display
        display_name = partner.replace("@", "")
        keyboard.append([
            InlineKeyboardButton(
                text=f"Партнёр {i}", 
                url=f"https://t.me/{display_name}"
            )
        ])
    
    keyboard.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
