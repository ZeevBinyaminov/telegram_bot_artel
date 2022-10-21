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
                 "orders (user_tag VARCHAR(128), subject VARCHAR(128), "
                 "status BOOL, details TEXT")

    base.execute("CREATE TABLE IF NOT EXISTS "
                 "performers (user_tag VARCHAR(128), subject VARCHAR(128), "
                 "skills TEXT, full_name VARCHAR(128))")

    base.execute("CREATE TABLE IF NOT EXISTS "
                 "others (user_tag VARCHAR(128), suggestions TEXT)")
    base.commit()


async def sql_add_command(table_name, state):
    async with state.proxy() as data:
        cur.execute(f"INSERT INTO {table_name} VALUES {tuple(data.values())}")
        base.commit()


async def sql_read_command(message: types.Message):
    message_text, table_name = message.text.split()
    for ret in cur.execute(f"SELECT * FROM {table_name}").fetchall():
        await message.answer(ret)
