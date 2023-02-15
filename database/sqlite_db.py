# import json
#
# from aiogram import types
#
# from database import database
#
# # database = database.Database("artel.db")
# db = database.database
# base = db.base
# cur = db.cursor
#
#
#
#
#
# async def sql_read_command(message: types.Message):
#     message_text, *info = message.text.strip().split()
#
#     if info:
#         table_name = info[0]
#         if table_name in ["orders", "performers", "others"]:
#             table = cur.execute(f"SELECT * FROM {table_name}").fetchall()
#             if table:
#                 for row in table:
#                     await message.answer(row)
#             else:
#                 await message.answer(f"Таблица \"{table_name}\" пустая")
#         else:
#             await message.answer("Нет такой таблицы")
#     else:
#         await message.answer("Неправильный формат: введите \"получить название таблицы\"")
