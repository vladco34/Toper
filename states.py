from aiogram.fsm.state import State, StatesGroup

class UserStates(StatesGroup):
    """States for user interactions"""
    waiting_for_code = State()
    needs_subscription = State()

class AdminStates(StatesGroup):
    """States for admin interactions"""
    # Adding movie states
    waiting_for_movie_code = State()
    waiting_for_movie_title = State()
    waiting_for_movie_poster = State()
    waiting_for_movie_episodes = State()
    
    # Deleting movie state
    waiting_for_delete_code = State()
    
    # Partner management states
    waiting_for_partner_link = State()
