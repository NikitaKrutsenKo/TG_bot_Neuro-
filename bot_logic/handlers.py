from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

import bot_logic.keyboards as kb
import bot_logic.database.requests as rq
import bot_logic.database.models as models
import bot_logic.user_states as user_states
from aiogram.fsm.context import FSMContext

from globals import TOKEN

import re

router = Router()

#===============================================================
@router.message(Command('admin'))
async def get_password_admin(message : Message, state : FSMContext):
    await state.set_state(user_states.GrantAdmin.get_password)
    await message.answer('Пароль: ')


@router.message(user_states.GrantAdmin.get_password)
async def validate_password_admin(message : Message, state : FSMContext):
    await state.clear()
    if message.text == TOKEN:
        await rq.grant_user_admin(message.from_user.id)
        await message.answer('Доступ дозволено')
    else:
        await message.answer('У доступі відмовлено')

#===============================================================

@router.message(Command('start'))
async def send_welcome(message: Message):
    await rq.set_user(message.from_user.id)
    await message.reply("Доброї днини, пункти головного меню перед вами " + "\nякщо ви адмін, то пропишіть:\n /start_admin", 
    reply_markup = kb.main_features_keyboard)


#===============================================================Пункти головного меню
@router.message(lambda message: message.text in kb.main_features_list)
async def features_list(message: Message):
    feature = kb.main_features_list.get(message.text, None)
    if feature:
        await message.answer(' Ви обрали ' + message.text, reply_markup = await feature())
    else:
        await message.answer('Сталася помилка, спробуйте ще раз')

#===============================================================

#===============================================================Нейронки
@router.callback_query(F.data.startswith('neuro_type_'))
async def show_neyro_types(callback : CallbackQuery):

    neyro_type_id = int(re.search(r'\d+', callback.data).group())
    neyro_type = await rq.get_neuro_type_by_id(neyro_type_id)
    if neyro_type:
        await callback.answer(None)
        await callback.message.answer('Ви обрали категорію '+ neyro_type.name, reply_markup=await kb.networks_by_type_keyboard(neyro_type_id))
    else:
        await callback.answer(None)
        await callback.message.answer('Сталася помилка, спробуйте ще раз')


@router.callback_query(F.data.startswith('network_'))
async def show_neural_network_info(callback: CallbackQuery):
    neural_network_id = int(re.search(r'\d+', callback.data).group())
    neural_network = await rq.get_network_by_id(neural_network_id)
    if neural_network:
        await callback.answer(None)
        await callback.message.answer(info_message_for_network(neural_network),  parse_mode='Markdown')
    else:
        await callback.answer(None)
        await callback.message.answer('Сталася помилка, спробуйте ще раз')


def info_message_for_network(neural_network : models.NeuralNetwork) -> str:
    
    name = neural_network.name
    description = neural_network.description
    neuro_ref = neural_network.neuro_ref
    neuro_vid_tutorial = neural_network.neuro_video_tutorial
    neuro_message_ref = neural_network.neuro_message_ref

    part_name = {
    '#Назва' : name,
    '#Опис' : description,    
    '#Відео' : neuro_vid_tutorial, 
    '#Деталі \n Інші цікаві штуки можна почитати [тут]' : neuro_message_ref,
    '#Посилання' : neuro_ref,
    }

    result_lines = []

    for key, value in part_name.items():
        if value is not None:
            result_lines.append(f"{key}\n{value}\n")

    result_string = "\n".join(result_lines)

    return result_string





#===============================================================

