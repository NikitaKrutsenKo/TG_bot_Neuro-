from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
import bot_logic.database.requests as rq 
import bot_logic.database.models as models
from bot_logic.keyboards import user_features_list


#=============================================================

async def create_admin_feature_keyboard():
    keyboard = ReplyKeyboardBuilder()
    
    for item in user_features_list:
        keyboard.add(KeyboardButton(text=item))
    
    for item in admin_features_list:
        keyboard.add(KeyboardButton(text=item))

    ready_keyboard = keyboard.adjust(2).as_markup()
    ready_keyboard.input_field_placeholder = 'Оберіть задачу'
    ready_keyboard.resize_keyboard = True
    return ready_keyboard


async def admin_commands_keyboard():
    keyboard = ReplyKeyboardBuilder()
    for c in admin_commands_list:
        keyboard.add(KeyboardButton(text=c))
    keyboard.add(KeyboardButton(text='На головну'))

    ready_keyboard = keyboard.adjust(2).as_markup()
    ready_keyboard.input_field_placeholder = 'Оберіть задачу'
    ready_keyboard.resize_keyboard = True
    return ready_keyboard


admin_features_list = {
    'Команди' : admin_commands_keyboard
}

admin_commands_list = {
    '/add_new_neuro' : 'додати нову нейронку',
    '/edit_neuro' : 'змінити якусь конкретну нейронку',
    '/delete_neuro_type' : 'видалити тип нейронки',
    '/delete_neuro' : 'видалити конкретну нейронку'
}

#=============================================================



async def choose_neuro_types_keyboard():
    all_types = await rq.get_neuro_types()
    keyboard = InlineKeyboardBuilder()
    for t in all_types:
        keyboard.add(InlineKeyboardButton(text=t.name, callback_data=f"choose_neuro_type_{t.id}"))
    keyboard.add(InlineKeyboardButton(text='СТВОРИТИ НОВИЙ', callback_data="choose_neuro_type_new"))
    return keyboard.adjust(1).as_markup()


async def delete_neuro_type_keyboard():
    all_types = await rq.get_neuro_types()
    keyboard = InlineKeyboardBuilder()
    for t in all_types:
        keyboard.add(InlineKeyboardButton(text=t.name, callback_data=f'delete_neuro_type_{t.id}'))
    return keyboard.adjust(1).as_markup()


async def update_neuro_networks_keyboard():
    all_networks = await rq.get_all_neuro()
    keyboard = InlineKeyboardBuilder()
    for n in all_networks:
        keyboard.add(InlineKeyboardButton(text=n.name, callback_data=f"start_update_neuro_{n.id}"))
    return keyboard.adjust(1).as_markup()

async def delete_neuro_networks_keyboard():
    all_networks = await rq.get_all_neuro()
    keyboard = InlineKeyboardBuilder()
    for n in all_networks:
        keyboard.add(InlineKeyboardButton(text=n.name, callback_data=f"delete_neuro_network_{n.id}"))
    return keyboard.adjust(1).as_markup()


async def all_network_info(network : models.NeuralNetwork):
    neuro_type = await rq.get_neuro_type_by_id(network.neuro_type)
    neuro_type_name = None
    if neuro_type != None:
        neuro_type_name = neuro_type.name

    keyboard = InlineKeyboardBuilder()    
    keyboard.add(InlineKeyboardButton(text=f'#Назва: {network.name}', 
    callback_data="update_neuro_name"))

    keyboard.add(InlineKeyboardButton(text=f'#Опис: {truncate_string(network.description)}', 
    callback_data="update_neuro_description"))

    keyboard.add(InlineKeyboardButton(text=f'#Тип: {neuro_type_name}', 
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