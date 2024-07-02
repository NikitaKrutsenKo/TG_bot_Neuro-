import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os
from bot_logic import handlers

load_dotenv()
TOKEN = os.getenv("TOKEN")

async def main():
    bot = Bot(token= TOKEN)
    dispatcher = Dispatcher()
    dispatcher.include_router(router=handlers.router)
    await dispatcher.start_polling(bot)


if __name__ == '__main__': 
    asyncio.run(main())
