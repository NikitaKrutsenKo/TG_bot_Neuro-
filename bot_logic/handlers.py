from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from .keyboards import topics, custom_keyboard

router = Router()

@router.message(Command('start'))
async def send_welcome(message: Message):
    await message.reply("Привіт, це тестова версія кнопок, виберіть тему:", reply_markup = custom_keyboard)

@router.message(lambda message: message.text in topics)
async def send_topic_message(message: Message):
    topic_message = topics.get(message.text, "Тема не знайдена")
    await message.reply(topic_message, parse_mode='Markdown')



