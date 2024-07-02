from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

class Register(StatesGroup):
    user_name = State()
    user_password = State()

