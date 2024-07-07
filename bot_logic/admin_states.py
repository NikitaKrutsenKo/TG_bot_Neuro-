from aiogram.fsm.state import StatesGroup, State

class CreateNewNeuro(StatesGroup):
    name = State()
    description = State()
    
    neuro_type = State()
    new_neuro_type = State()

    neuro_video_tutorial = State()
    neuro_message_ref = State()
    neuro_ref = State()
    is_available = State()


class UpdateNeuro(StatesGroup):
    update_start = State()

    new_name = State()
    new_description = State()

    update_neuro_type = State()
    new_update_neuro_type = State()

    update_neuro_video_tutorial = State()
    update_neuro_message_ref = State()
    update_neuro_ref = State()
    update_is_available = State()