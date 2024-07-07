import asyncio
from aiogram import Bot, Dispatcher

from bot_logic import handlers, admin_handlers
from bot_logic.database.models import async_db_create

from globals import TOKEN
from keep_alive import keep_alive

keep_alive()


async def main():
    await async_db_create()
    bot = Bot(token= TOKEN)
    dispatcher = Dispatcher()
    dispatcher.include_routers(handlers.router, admin_handlers.admin_router)
    await dispatcher.start_polling(bot)


if __name__ == '__main__': 
    asyncio.run(main())
