from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from config import MESSAGES
from states import UserStates
from keyboards import (
    main_menu_keyboard, 
    subscription_check_keyboard, 
    back_to_menu_keyboard,
    movie_episodes_keyboard,
    partners_list_keyboard,
    partners_subscription_keyboard
)
from data_manager import data_manager

router = Router()

@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    """Handle /start command"""
    await state.clear()
    
    partners = data_manager.get_partners()
    
    if partners:
        # Set state that user needs subscription
        await state.set_state(UserStates.needs_subscription)
        
        # Format partners list with numbers
        partners_text = "\n".join([f"Партнёр {i}" for i, partner in enumerate(partners, 1)])
        text = f"""📢 Чтобы пользоваться ботом, подпишись на всех партнёров:

{partners_text}

После подписки нажми кнопку "✅ Проверить подписку\""""
        keyboard = partners_subscription_keyboard(partners)
    else:
        # No partners, show main menu
        text = "🎬 Добро пожаловать! Выберите действие из меню:"
        keyboard = main_menu_keyboard()
    
    await message.answer(text, reply_markup=keyboard)

@router.callback_query(F.data == "check_subscription")
async def check_subscription(callback: CallbackQuery, state: FSMContext):
    """Handle subscription check (simplified)"""
    await state.clear()
    text = "🎬 Добро пожаловать! Выберите действие из меню:"
    keyboard = main_menu_keyboard()
    
    if callback.message:
        await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data == "search_content")
async def search_content(callback: CallbackQuery, state: FSMContext):
    """Start content search"""
    current_state = await state.get_state()
    
    # Check if user needs subscription
    if current_state == UserStates.needs_subscription:
        partners = data_manager.get_partners()
        if partners:
            partners_text = "\n".join([f"Партнёр {i}" for i, partner in enumerate(partners, 1)])
            text = f"""📢 Сначала подпишись на всех партнёров:

{partners_text}

После подписки нажми кнопку "✅ Проверить подписку\""""
            keyboard = partners_subscription_keyboard(partners)
            if callback.message:
                await callback.message.edit_text(text, reply_markup=keyboard)
            await callback.answer()
            return
    
    await state.set_state(UserStates.waiting_for_code)
    
    text = MESSAGES["enter_code"]
    keyboard = back_to_menu_keyboard()
    
    if callback.message:
        await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@router.message(UserStates.waiting_for_code)
async def process_search_code(message: Message, state: FSMContext):
    """Process entered movie code"""
    if not message.text:
        return
    code = message.text.strip()
    movie = data_manager.get_movie(code)
    
    if movie:
        # Movie found, show details
        text = f"🎬 <b>{movie['title']}</b>"
        
        # Send poster if available
        if movie.get('poster'):
            try:
                await message.answer_photo(
                    photo=movie['poster'],
                    caption=text
                )
            except Exception:
                # If poster fails, send as text
                await message.answer(text)
        else:
            await message.answer(text)
        
        # Send episodes if available
        if movie.get('episodes'):
            episodes = [ep.strip() for ep in movie['episodes'] if ep.strip()]
            if episodes:
                keyboard = movie_episodes_keyboard(episodes)
                await message.answer(
                    "🎞️ Выберите эпизод:",
                    reply_markup=keyboard
                )
            else:
                keyboard = back_to_menu_keyboard()
                await message.answer(
                    "📺 Эпизоды скоро будут добавлены!",
                    reply_markup=keyboard
                )
        else:
            keyboard = back_to_menu_keyboard()
            await message.answer(
                "📺 Эпизоды скоро будут добавлены!",
                reply_markup=keyboard
            )
        
        await state.clear()
    else:
        # Movie not found
        text = MESSAGES["code_not_found"]
        keyboard = back_to_menu_keyboard()
        
        await message.answer(text, reply_markup=keyboard)

@router.callback_query(F.data == "show_partners")
async def show_partners(callback: CallbackQuery, state: FSMContext):
    """Show partners list"""
    current_state = await state.get_state()
    
    # Check if user needs subscription
    if current_state == UserStates.needs_subscription:
        partners = data_manager.get_partners()
        if partners:
            partners_text = "\n".join([f"Партнёр {i}" for i, partner in enumerate(partners, 1)])
            text = f"""📢 Сначала подпишись на всех партнёров:

{partners_text}

После подписки нажми кнопку "✅ Проверить подписку\""""
            keyboard = partners_subscription_keyboard(partners)
            if callback.message:
                await callback.message.edit_text(text, reply_markup=keyboard)
            await callback.answer()
            return
    
    partners = data_manager.get_partners()
    
    if partners:
        text = "👥 <b>Наши партнёры:</b>"
        keyboard = partners_list_keyboard(partners)
    else:
        text = MESSAGES["no_partners"]
        keyboard = back_to_menu_keyboard()
    
    if callback.message:
        await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data == "show_help")
async def show_help(callback: CallbackQuery, state: FSMContext):
    """Show help message"""
    current_state = await state.get_state()
    
    # Check if user needs subscription
    if current_state == UserStates.needs_subscription:
        partners = data_manager.get_partners()
        if partners:
            partners_text = "\n".join([f"Партнёр {i}" for i, partner in enumerate(partners, 1)])
            text = f"""📢 Сначала подпишись на всех партнёров:

{partners_text}

После подписки нажми кнопку "✅ Проверить подписку\""""
            keyboard = partners_subscription_keyboard(partners)
            if callback.message:
                await callback.message.edit_text(text, reply_markup=keyboard)
            await callback.answer()
            return
    
    text = MESSAGES["help_message"]
    keyboard = back_to_menu_keyboard()
    
    if callback.message:
        await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery, state: FSMContext):
    """Return to main menu"""
    current_state = await state.get_state()
    
    # Check if user needs subscription
    if current_state == UserStates.needs_subscription:
        partners = data_manager.get_partners()
        if partners:
            partners_text = "\n".join([f"Партнёр {i}" for i, partner in enumerate(partners, 1)])
            text = f"""📢 Сначала подпишись на всех партнёров:

{partners_text}

После подписки нажми кнопку "✅ Проверить подписку\""""
            keyboard = partners_subscription_keyboard(partners)
            if callback.message:
                await callback.message.edit_text(text, reply_markup=keyboard)
            await callback.answer()
            return
    
    await state.clear()
    
    text = "🎬 Главное меню. Выберите действие:"
    keyboard = main_menu_keyboard()
    
    if callback.message:
        await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()