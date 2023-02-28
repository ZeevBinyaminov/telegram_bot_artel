from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from database import database
from loader import bot, ADMIN_ID, DASHA_ID, ABRAM_ID, KIRILL_ID


def is_admin(user_id):
    return user_id in (ADMIN_ID, DASHA_ID, ABRAM_ID, KIRILL_ID)


async def get_table(message: types.Message):
    if is_admin(message.from_user.id):
        message_text, *info = message.text.strip().split()
        if info:
            table_name = info[0]
            if table_name in ["orders", "performers", "others", "perf_description"]:
                table = database.database.cursor.execute(f"SELECT * FROM {table_name}").fetchall()
                if table:
                    for row in table:
                        await message.answer(row)
                else:
                    await message.answer(f"Таблица \"{table_name}\" пустая")
            else:
                await message.answer("Нет такой таблицы")
        else:
            await message.answer("Неправильный формат: введите \"получить название таблицы\"")


def parse_file(file_id):
    pass


async def write_performers(message: types.Message):
    if is_admin(message.from_user.id):
        await message.answer("файл получен")
        parse_file(message.document.file_id)


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(get_table, commands=['получить'], state=None)
    dp.register_message_handler(get_table, Text(contains='получить', ignore_case=True), state=None)
    dp.register_message_handler(write_performers, content_types=["document"], state=None)
