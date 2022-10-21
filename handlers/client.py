from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from loader import dp
from database import sqlite_db


async def send_welcome(message: types.Message):
    await message.reply("Привет! Я чат-бот Артель.\nЧем могу помочь?")  # reply_markup=''


# check mindmap
class FSMClient(StatesGroup):
    # client branch
    status = State()
    premium = State()
    subject = State()
    details = State()
    # performer branch
    performer = State()
    subjects = State()
    # other branch
    other = State()
    suggestions = State()
    # finish state


async def client_fsm_start(message: types.Message):
    # await FSMClient.first.set()
    await message.reply('FSM запущена\nВведи текст к первому')



def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start', 'help'])

