from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot_logic.database.requests import get_neuro_types


async def choose_neuro_types_keyboard():
    all_types = await get_neuro_types()
    keyboard = InlineKeyboardBuilder()
    for t in all_types:
        keyboard.add(InlineKeyboardButton(text=t.name, callback_data=f"choose_neuro_type_{t.id}"))
    keyboard.add(InlineKeyboardButton(text='СТВОРИТИ НОВИЙ', callback_data=f"choose_neuro_tupe_new"))
    return keyboard.adjust(1).as_markup()