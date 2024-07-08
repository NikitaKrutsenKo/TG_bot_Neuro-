from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from bot_logic.database.requests import get_neuro_types, get_neuro_by_type

async def create_user_feature_keyboard():
    keyboard = ReplyKeyboardBuilder()
    
    for item in user_features_list:
        keyboard.add(KeyboardButton(text=item))

    ready_keyboard = keyboard.adjust(2).as_markup()
    ready_keyboard.input_field_placeholder = 'Оберіть задачу'
    ready_keyboard.resize_keyboard = True
    return ready_keyboard


#===============================================================Нейронки
async def neuro_types_keyboard():
    all_types = await get_neuro_types()
    keyboard = InlineKeyboardBuilder()
    for t in all_types:
        keyboard.add(InlineKeyboardButton(text=t.name, callback_data=f"neuro_type_{t.id}"))
    return keyboard.adjust(2).as_markup()


async def networks_by_type_keyboard(neuro_type: int):
    all_networks = await get_neuro_by_type(neuro_type)
    keyboard = InlineKeyboardBuilder()
    for n in all_networks:
        if n.is_available == True:
            keyboard.add(InlineKeyboardButton(text=n.name, callback_data=f"network_{n.id}"))
    return keyboard.adjust(2).as_markup()

#===============================================================


user_features_list = {
    'Навігатор': neuro_types_keyboard,
    'Профіль' : None
}