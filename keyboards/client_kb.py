from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from loader import bot
from database.sqlite_db import sql_execute

# start menu keyboard
help_button = KeyboardButton('/help')
main_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
main_menu.add(help_button)

# inline keyboard markup
user_inkb = InlineKeyboardMarkup(row_width=1)

become_client = InlineKeyboardButton(text="Хочу купить работу",
                                     callback_data='become client')
become_performer = InlineKeyboardButton(text="Хочу стать вашим исполнителем",
                                        callback_data='become performer')
become_other = InlineKeyboardButton(text="Другое",
                                    callback_data='become other')
cancel_button = InlineKeyboardButton(text="Отмена",
                                     callback_data='cancel')

cancel_inkb = InlineKeyboardMarkup().add(cancel_button)
user_inkb.add(become_client, become_performer, become_other)

subjects_inkb = InlineKeyboardMarkup(row_width=2)
subjects_list = ['Математика', 'История', 'Социология',
                 'Политология', 'Международные отношения',
                 'Право', 'Государственное управление',
                 'Урабанистика', 'Философия', 'Филология',
                 'Экономика', 'Программирование', 'Другое']
for subject in subjects_list:
    subjects_inkb.insert(InlineKeyboardButton(text=subject, callback_data=subject))
subjects_inkb.add(cancel_button)


price_button = KeyboardButton('/price')
price_kb = ReplyKeyboardMarkup(one_time_keyboard=True).add(price_button)

# async def price_keyboard(chat_id, order_id):
#     price_button = KeyboardButton('/price')
#     price_kb = ReplyKeyboardMarkup().add(price_button)
#     await bot.send_message(chat_id=chat_id,
#                            text=sql_execute(f"SELECT * FROM orders WHERE order_id = {order_id}").fetchmany(1),
#                            reply_markup=price_kb)


# subjects_id = {
#     "Математика": -1001763954483
# }
#
#
# async def send_order_form(subject_name, order_info: tuple):
#     bot.send_message(text='Новый заказ, детали:\n' + order_info[2],
#                      chat_id=subjects_id[subject_name],
#                      reply_markup=price_keyboard)
