import logging
from aiogram import executor

from loader import bot, dp, ADMIN_ID
from handlers import client, admin
from database import sqlite_db
logging.basicConfig(level=logging.INFO)


async def on_startup(dp):
    await bot.send_message(chat_id=ADMIN_ID, text='Бот запущен!')
    sqlite_db.sql_start()


async def on_shutdown(dp):
    await bot.send_message(chat_id=ADMIN_ID, text='Бот выключен!')

client.register_callbacks_and_handlers_client(dp)
admin.register_handlers_admin(dp)

if __name__ == '__main__':
    executor.start_polling(dp,
                           on_startup=on_startup,
                           on_shutdown=on_shutdown,
                           skip_updates=True)
