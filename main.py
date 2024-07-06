import asyncio
from aiogram import Bot, Dispatcher

from dotenv import load_dotenv
import os

from bot_logic import handlers, admin_handlers
from bot_logic.database.models import async_db_create

load_dotenv()
TOKEN = os.getenv("TOKEN")

async def main():
    await async_db_create()
    bot = Bot(token= TOKEN)
    dispatcher = Dispatcher()
    dispatcher.include_routers(handlers.router, admin_handlers.admin_router)
    await dispatcher.start_polling(bot)


if __name__ == '__main__': 
    asyncio.run(main())
