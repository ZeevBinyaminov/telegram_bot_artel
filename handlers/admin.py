from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from loader import dp


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
    # sql_add(state) # функция для записи в бд
    await state.finish()


async def cancel_handler(message: types.Message, state=FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("Заказ отменен.\nЕсли хотите начать сначала, введите /start")


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cancel_handler, state="*", commands='отмена')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(fsm_start, commands=['checkfsm'], state=None)
    dp.register_message_handler(get_first, state=FSMAdmin.first)
    dp.register_message_handler(get_third, state=FSMAdmin.third)


