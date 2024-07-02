from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from .keyboards import (
main_features_keyboard, 
main_features_list,
neuro_type_list
)

router = Router()

@router.message(Command('start'))
async def send_welcome(message: Message):
    await message.reply("Привіт, це тестова версія кнопок, виберіть задачу:", reply_markup = main_features_keyboard)


@router.message(lambda message: message.text in main_features_list)
async def send_feature_menu(message: Message):
    feature_type = main_features_list.get(message.text, None)
    if feature_type != None:
        await message.answer('Ви перейшли у меню задачі '+ message.text + '. Оберіть наступну дію', reply_markup = feature_type)
    else:
        await message.answer('Або такої задачі нема, або сталася помилка. Спробуйте ще раз')


@router.message(lambda message: message.text in neuro_type_list)
async def send_topic_message(message: Message):
    neuro_type_message = neuro_type_list.get(message.text, "Тема не знайдена")
    await message.reply(neuro_type_message, parse_mode='Markdown')



