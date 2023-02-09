import sqlite3 as sq
from aiogram import types
from loader import bot, ADMIN_ID, ABRAM_ID, DASHA_ID, KIRILL_ID


def sql_start():
    global base, cur
    base = sq.connect("artel.db")
    cur = base.cursor()
    if base:
        print('Database connected!')

    base.execute("CREATE TABLE IF NOT EXISTS "
                 "orders (user_tag VARCHAR(64) NOT NULL, "
                 "subject VARCHAR(128) NOT NULL, order_details TEXT, "
                 "order_id VARCHAR(64), message_id VARCHAR(64))")

    base.execute("CREATE TABLE IF NOT EXISTS "
                 "performers (user_tag VARCHAR(64) NOT NULL, "
                 "performer_id VARCHAR(64), "
                 "subject VARCHAR(128) NOT NULL, "
                 "performer_details TEXT, is_busy INTEGER DEFAULT 0)")

    base.execute("CREATE TABLE IF NOT EXISTS "
                 "others (user_tag VARCHAR(64) NOT NULL, "
                 "suggestions TEXT)")

    base.execute("CREATE TABLE IF NOT EXISTS "
                 "perf_description "
                 "(performer_id VARCHAR(64) NOT NULL, "
                 "description TEXT NOT NULL)")

    base.execute("CREATE TABLE IF NOT EXISTS "
                 "chats (chat_id INTEGER PRIMARY KEY AUTOINCREMENT, "
                 "chat_one VARHCAR(64) NOT NULL, "
                 "chat_two VARHCAR(64) NOT NULL)")

    base.commit()


async def notify(data: dict):
    message_text = "Пришел новый заказ:\n" + '\n'.join(data.values())
    for admin_id in (ADMIN_ID, ABRAM_ID, DASHA_ID, KIRILL_ID):
        await bot.send_message(
            chat_id=admin_id,
            text=message_text
        )


async def sql_add_command(table_name, state):
    async with state.proxy() as data:
        cur.execute("INSERT INTO %s %s VALUES %s" %
                    (table_name, tuple(data.keys()), tuple(data.values())))

        # await notify(data=data)
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


def sql_select(command, values):
    return cur.execute(command, values).fetchmany(1)


def sql_execute(command, values):
    cur.execute(command, values)
    cur.connection.commit()


def get_active_chat(user_id):
    chat_id = sql_select("SELECT chat_two "
                         "FROM chats "
                         "WHERE chat_one = ?", (user_id,))
    if not chat_id:
        chat_id = sql_select("SELECT chat_one "
                             "FROM chats "
                             "WHERE chat_two = ?", (user_id,))
    return chat_id[0][0] if chat_id else 0
