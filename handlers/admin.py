from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from database import sqlite_db


async def cancel_handler(message: types.Message, state=FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.reply("Нечего отменять")
        return
    await state.finish()
    await message.reply("Заказ отменен.\nЕсли хотите начать сначала, введите /start")


async def sql_select_command(message: types.Message):
    await sqlite_db.sql_read_command(message)


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(sql_select_command, commands=['получить'], state=None)
    dp.register_message_handler(sql_select_command, Text(contains='получить', ignore_case=True), state=None)

    dp.register_message_handler(cancel_handler, state="*", commands='отмена')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")

