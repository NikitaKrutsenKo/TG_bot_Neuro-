from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

class GrantAdmin(StatesGroup):
    get_password = State()