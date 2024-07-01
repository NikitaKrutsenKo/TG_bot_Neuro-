import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = Bot(token= TOKEN)
dispatcher = Dispatcher()

@dispatcher.message()
async def new_command(message: Message):
    await message.answer('Йоу, як справи ' +  message.from_user.username + ' це тестова версія боту 1.0.0, він поки нічого не вміє :)')


async def main():
    await dispatcher.start_polling(bot)


if __name__ == '__main__': 
    asyncio.run(main())
