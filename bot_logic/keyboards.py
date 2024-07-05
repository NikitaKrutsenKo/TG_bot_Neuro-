from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot_logic.database.requests import get_neuro_types, get_networks_by_type

main_features_keyboard = ReplyKeyboardMarkup(keyboard=
        [[KeyboardButton(text='Навігатор')], [KeyboardButton(text='Профіль')]],        
    resize_keyboard=True, 
    input_field_placeholder='Оберіть задачу'
)


#===============================================================Нейронки
async def neuro_types_keyboard():
    all_types = await get_neuro_types()
    keyboard = InlineKeyboardBuilder()
    for t in all_types:
        keyboard.add(InlineKeyboardButton(text=t.name, callback_data=f"neuro_type_{t.id}"))
    return keyboard.adjust(2).as_markup()


async def networks_by_type_keyboard(neuro_type: int):
    all_networks = await get_networks_by_type(neuro_type)
    keyboard = InlineKeyboardBuilder()
    for n in all_networks:
        keyboard.add(InlineKeyboardButton(text=n.name, callback_data=f"network_{n.id}"))
    return keyboard.adjust(2).as_markup()

#===============================================================


main_features_list = {
    'Навігатор': neuro_types_keyboard,
    'Профіль' : None
}