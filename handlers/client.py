from aiogram import types, Dispatcher
from loader import dp


# @dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я чат-бот Артель.\nЧем могу помочь?") # reply_markup=''


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start', 'help'])
