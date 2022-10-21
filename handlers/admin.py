from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from loader import dp
from database import sqlite_db


# check mindmap
class FSMAdmin(StatesGroup):
    first = State()
    second = State()
    third = State()


async def fsm_start(message: types.Message):
    await FSMAdmin.first.set()
    await message.reply('FSM запущена\nВведи текст к первому')


async def get_first(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['first_text'] = message.text
    await FSMAdmin.third.set()
    await message.reply(f"Текст к первому: {message.text}")
    await message.reply("теперь введи текст к третьему")


async def get_third(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['third_text'] = message.text
    await message.reply(f"Текст к третьему: {message.text}\nFSM завершила работу")
    await sqlite_db.sql_add_command(state=state, table_name='test')
    await state.finish()


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
    dp.register_message_handler(cancel_handler, state="*", commands='отмена')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(fsm_start, commands=['checkfsm'], state=None)
    dp.register_message_handler(get_first, state=FSMAdmin.first)
    dp.register_message_handler(get_third, state=FSMAdmin.third)
    #
    dp.register_message_handler(sql_select_command, commands=['получить'], state=None)
    dp.register_message_handler(sql_select_command,
                                Text(contains='получить', ignore_case=True), state=None)#, is_chat_admin=True)
