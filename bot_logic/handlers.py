from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

import bot_logic.keyboards as kb
import bot_logic.database.requests as rq
import bot_logic.admin_handlers as admin_handlers

import re

router = Router()

@router.message(Command('start'))
async def send_welcome(message: Message):
    await rq.set_user(message.from_user.id)
    await message.reply("Доброї днини, пункти головного меню перед вами " + "\nякщо ви адмін, то пропишіть:\n /start_admin"
                        , reply_markup = kb.main_features_keyboard)


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
        await callback.message.answer('Назва: ' + neural_network.name + '\n'
                                    'Опис: \n' + neural_network.description)
    else:
        await callback.answer(None)
        await callback.message.answer('Сталася помилка, спробуйте ще раз')
#===============================================================

