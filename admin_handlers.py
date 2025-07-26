from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from config import ADMIN_USERNAME, MESSAGES
from states import AdminStates
from keyboards import (
    admin_menu_keyboard,
    partners_management_keyboard,
    back_to_menu_keyboard
)
from data_manager import data_manager

router = Router()

def is_admin(message_or_callback) -> bool:
    """Check if user is admin"""
    if hasattr(message_or_callback, 'from_user'):
        user = message_or_callback.from_user
    else:
        user = message_or_callback.message.from_user if hasattr(message_or_callback, 'message') and message_or_callback.message else None
    
    return user is not None and user.username == ADMIN_USERNAME

@router.message(Command("admin"))
async def admin_command(message: Message, state: FSMContext):
    """Handle /admin command"""
    if not is_admin(message):
        await message.answer("❌ У вас нет доступа к админ-панели.")
        return
    
    await state.clear()
    text = MESSAGES["admin_menu"]
    keyboard = admin_menu_keyboard()
    
    await message.answer(text, reply_markup=keyboard)

@router.callback_query(F.data == "admin_menu")
async def admin_menu_callback(callback: CallbackQuery, state: FSMContext):
    """Return to admin menu"""
    if not is_admin(callback):
        await callback.answer("❌ У вас нет доступа к админ-панели.", show_alert=True)
        return
    
    await state.clear()
    text = MESSAGES["admin_menu"]
    keyboard = admin_menu_keyboard()
    
    if callback.message:
        await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data == "admin_add_movie")
async def admin_add_movie(callback: CallbackQuery, state: FSMContext):
    """Start adding movie process"""
    if not is_admin(callback):
        await callback.answer("❌ У вас нет доступа к админ-панели.", show_alert=True)
        return
    
    await state.set_state(AdminStates.waiting_for_movie_code)
    
    text = MESSAGES["enter_movie_code"]
    if callback.message:
        await callback.message.edit_text(text)
    await callback.answer()

@router.message(AdminStates.waiting_for_movie_code)
async def process_movie_code(message: Message, state: FSMContext):
    """Process movie code input"""
    if not is_admin(message):
        return
    
    if not message.text:
        return
        
    code = message.text.strip()
    await state.update_data(code=code)
    await state.set_state(AdminStates.waiting_for_movie_title)
    
    await message.answer(MESSAGES["enter_movie_title"])

@router.message(AdminStates.waiting_for_movie_title)
async def process_movie_title(message: Message, state: FSMContext):
    """Process movie title input"""
    if not is_admin(message):
        return
    
    if not message.text:
        return
        
    title = message.text.strip()
    await state.update_data(title=title)
    await state.set_state(AdminStates.waiting_for_movie_poster)
    
    await message.answer(MESSAGES["enter_movie_poster"])

@router.message(AdminStates.waiting_for_movie_poster)
async def process_movie_poster(message: Message, state: FSMContext):
    """Process movie poster input"""
    if not is_admin(message):
        return
    
    if not message.text:
        return
        
    poster = message.text.strip()
    await state.update_data(poster=poster)
    await state.set_state(AdminStates.waiting_for_movie_episodes)
    
    await message.answer(MESSAGES["enter_movie_episodes"])

@router.message(AdminStates.waiting_for_movie_episodes)
async def process_movie_episodes(message: Message, state: FSMContext):
    """Process movie episodes input"""
    if not is_admin(message):
        return
    
    if not message.text:
        return
        
    episodes_text = message.text.strip()
    episodes = [ep.strip() for ep in episodes_text.split(',') if ep.strip()]
    
    # Get saved data
    data = await state.get_data()
    code = data['code']
    title = data['title']
    poster = data['poster']
    
    # Save movie
    data_manager.add_movie(code, title, poster, episodes)
    
    await state.clear()
    
    text = MESSAGES["movie_added"]
    keyboard = admin_menu_keyboard()
    
    await message.answer(text, reply_markup=keyboard)

@router.callback_query(F.data == "admin_delete_movie")
async def admin_delete_movie(callback: CallbackQuery, state: FSMContext):
    """Start deleting movie process"""
    if not is_admin(callback):
        await callback.answer("❌ У вас нет доступа к админ-панели.", show_alert=True)
        return
    
    await state.set_state(AdminStates.waiting_for_delete_code)
    
    text = MESSAGES["enter_delete_code"]
    if callback.message:
        await callback.message.edit_text(text)
    await callback.answer()

@router.message(AdminStates.waiting_for_delete_code)
async def process_delete_code(message: Message, state: FSMContext):
    """Process delete code input"""
    if not is_admin(message):
        return
    
    if not message.text:
        return
        
    code = message.text.strip()
    
    if data_manager.delete_movie(code):
        text = MESSAGES["movie_deleted"]
    else:
        text = MESSAGES["movie_not_found_delete"]
    
    await state.clear()
    
    keyboard = admin_menu_keyboard()
    await message.answer(text, reply_markup=keyboard)

@router.callback_query(F.data == "admin_manage_partners")
async def admin_manage_partners(callback: CallbackQuery):
    """Show partners management"""
    if not is_admin(callback):
        await callback.answer("❌ У вас нет доступа к админ-панели.", show_alert=True)
        return
    
    partners = data_manager.get_partners()
    
    text = "🤝 <b>Управление партнёрами</b>\n\nТекущие партнёры:"
    if partners:
        text += "\n" + "\n".join([f"• {partner}" for partner in partners])
    else:
        text += "\n<i>Партнёров пока нет</i>"
    
    keyboard = partners_management_keyboard(partners)
    
    if callback.message:
        await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data.startswith("delete_partner:"))
async def delete_partner(callback: CallbackQuery):
    """Delete partner"""
    if not is_admin(callback):
        await callback.answer("❌ У вас нет доступа к админ-панели.", show_alert=True)
        return
    
    if not callback.data:
        return
        
    partner = callback.data.split(":", 1)[1]
    data_manager.delete_partner(partner)
    
    await callback.answer(MESSAGES["partner_deleted"])
    
    # Refresh partners list
    partners = data_manager.get_partners()
    
    text = "🤝 <b>Управление партнёрами</b>\n\nТекущие партнёры:"
    if partners:
        text += "\n" + "\n".join([f"• {partner}" for partner in partners])
    else:
        text += "\n<i>Партнёров пока нет</i>"
    
    keyboard = partners_management_keyboard(partners)
    if callback.message:
        await callback.message.edit_text(text, reply_markup=keyboard)

@router.callback_query(F.data == "add_partner")
async def add_partner(callback: CallbackQuery, state: FSMContext):
    """Start adding partner process"""
    if not is_admin(callback):
        await callback.answer("❌ У вас нет доступа к админ-панели.", show_alert=True)
        return
    
    await state.set_state(AdminStates.waiting_for_partner_link)
    
    text = MESSAGES["enter_partner_link"]
    if callback.message:
        await callback.message.edit_text(text)
    await callback.answer()

@router.message(AdminStates.waiting_for_partner_link)
async def process_partner_link(message: Message, state: FSMContext):
    """Process partner link input"""
    if not is_admin(message):
        return
    
    if not message.text:
        return
        
    partner = message.text.strip()
    
    # Ensure partner starts with @
    if not partner.startswith("@"):
        partner = "@" + partner
    
    data_manager.add_partner(partner)
    
    await state.clear()
    
    text = MESSAGES["partner_added"]
    keyboard = admin_menu_keyboard()
    
    await message.answer(text, reply_markup=keyboard)

@router.callback_query(F.data == "admin_statistics")
async def admin_statistics(callback: CallbackQuery):
    """Show statistics"""
    if not is_admin(callback):
        await callback.answer("❌ У вас нет доступа к админ-панели.", show_alert=True)
        return
    
    movies_count = data_manager.get_movies_count()
    partners_count = data_manager.get_partners_count()
    
    text = MESSAGES["statistics"].format(
        movies_count=movies_count,
        partners_count=partners_count
    )
    
    keyboard = admin_menu_keyboard()
    
    if callback.message:
        await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()