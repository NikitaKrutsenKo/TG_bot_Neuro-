from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

class CreateNewNeuro(StatesGroup):
    name = State()
    description = State()
    
    neuro_type = State()
    new_neuro_type = State()

    neuro_video_tutorial = State()
    neuro_message_ref = State()
    neuro_ref = State()
    is_available = State()

