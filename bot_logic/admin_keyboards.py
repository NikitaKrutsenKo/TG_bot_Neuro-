from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import bot_logic.database.requests as rq 
import bot_logic.database.models as models


async def choose_neuro_types_keyboard():
    all_types = await rq.get_neuro_types()
    keyboard = InlineKeyboardBuilder()
    for t in all_types:
        keyboard.add(InlineKeyboardButton(text=t.name, callback_data=f"choose_neuro_type_{t.id}"))
    keyboard.add(InlineKeyboardButton(text='СТВОРИТИ НОВИЙ', callback_data="choose_neuro_type_new"))
    return keyboard.adjust(1).as_markup()


async def update_neuro_networks_keyboard():
    all_networks = await rq.get_all_networks()
    keyboard = InlineKeyboardBuilder()
    for n in all_networks:
        keyboard.add(InlineKeyboardButton(text=n.name, callback_data=f"start_update_neuro_{n.id}"))
    return keyboard.adjust(1).as_markup()


async def all_network_info(network : models.NeuralNetwork):
    neuro_type_name = await rq.get_neuro_type_by_id(network.neuro_type)
    keyboard = InlineKeyboardBuilder()    
    keyboard.add(InlineKeyboardButton(text=f'#Назва: {network.name}', 
    callback_data="update_neuro_name"))

    keyboard.add(InlineKeyboardButton(text=f'#Опис: {truncate_string(network.description)}', 
    callback_data="update_neuro_description"))

    keyboard.add(InlineKeyboardButton(text=f'#Тип: {neuro_type_name.name}', 
    callback_data="update_neuro_type"))

    keyboard.add(InlineKeyboardButton(text=f'#Відео-тутор: {network.neuro_video_tutorial}', 
    callback_data="update_neuro_video"))

    keyboard.add(InlineKeyboardButton(text=f'#Повідомлення_з_чату: {network.neuro_message_ref}', 
    callback_data="update_neuro_message"))

    keyboard.add(InlineKeyboardButton(text=f'#Посилання: {network.neuro_ref}', 
    callback_data="update_neuro_ref"))

    keyboard.add(InlineKeyboardButton(text=f'#Доступність: {str(network.is_available)}', 
    callback_data="update_neuro_available"))
    return keyboard.adjust(1).as_markup()


def truncate_string(input_string, length=20):
    if len(input_string) > length:
        return input_string[:length] + '...'
    return input_string