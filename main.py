import asyncio
from aiogram import Bot, Dispatcher

from bot_logic import handlers
from bot_logic.admin_logic import admin_handlers
from bot_logic.database.models import async_db_create

from globals import TOKEN

from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def index():
    return "Alive"


def run():
    app.run(host='0.0.0.0', port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()


keep_alive()


async def main():
    await async_db_create()
    bot = Bot(token= TOKEN)
    dispatcher = Dispatcher()
    dispatcher.include_routers(handlers.router, admin_handlers.admin_router)
    await dispatcher.start_polling(bot)


if __name__ == '__main__': 
    asyncio.run(main())
