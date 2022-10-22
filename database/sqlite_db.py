import sqlite3 as sq
from aiogram import types
from loader import bot


def sql_start():
    global base, cur
    base = sq.connect("artel.db")
    cur = base.cursor()
    if base:
        print('Database connected!')

    base.execute("CREATE TABLE IF NOT EXISTS "
                 "orders (user_tag VARCHAR(64), is_premium BOOL, "
                 "subject VARCHAR(128), details TEXT)")

    base.execute("CREATE TABLE IF NOT EXISTS "
                 "performers (user_tag VARCHAR(64), subject VARCHAR(128), "
                 "skills TEXT)")

    base.execute("CREATE TABLE IF NOT EXISTS "
                 "others (user_tag VARCHAR(64), suggestions TEXT)")
    base.commit()


async def sql_add_command(table_name, state):
    async with state.proxy() as data:
        cur.execute(f"INSERT INTO {table_name} VALUES {tuple(data.values())}")
        base.commit()


async def sql_read_command(message: types.Message):
    message_text, *info = message.text.strip().split()

    if info:
        table_name = info[0]
        if table_name in ["orders", "performers", "others"]:
            table = cur.execute(f"SELECT * FROM {table_name}").fetchall()
            if table:
                for row in table:
                    await message.answer(row)
            else:
                await message.answer(f"Таблица \"{table_name}\" пустая")
        else:
            await message.answer("Нет такой таблицы")
    else:
        await message.answer("Неправильный формат: введите \"получить название таблицы\"")
