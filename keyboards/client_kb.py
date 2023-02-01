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

subjects_dict = {
    "Юриспруденция": -1001790959600,
    "Экономика": -1001852643314,
    "Политология": -1001679302522,
    "Социология": -1001608456987,
    "История": -1001804798141,
    "Философия": -1001806183269,
    "Психология": -1001631922451,
    "Программирование": -1001590590211,
    "Лингвистика и иностранные языки": -1001862273326,
    "Математика": -1001763954483,
    "Филология и литература": -1001823585368,
    "Искусство": -1001711068367,
    "Государственное управление": -1001881088844,
    "Международные отношения": -1001874994032,
    "Архитектура и урбанистика": -1001854906965,
    "Маркетинг и бизнес": -1001808316216,
    "Реклама и журналистика": -1001664717218,
    "Финансы, аудит и бухучет": -1001804298079,
    "Биология и медицина": -1001866691571,
    "Физика": -1001895191555,
    "Транскрипты": -1001810132774
}

subjects_inkb = InlineKeyboardMarkup(row_width=2)
for subject in subjects_dict:
    subjects_inkb.insert(InlineKeyboardButton(text=subject, callback_data=subject))
subjects_inkb.add(cancel_button)


price_button = InlineKeyboardButton(text="Предложить цену", callback_data="ask price")
price_inkb = InlineKeyboardMarkup(row_width=1)
price_inkb.add(price_button)


# async def price_keyboard(chat_id, order_id):
#     price_button = KeyboardButton('/price')
#     price_kb = ReplyKeyboardMarkup().add(price_button)
#     await bot.send_message(chat_id=chat_id,
#                            text=sql_execute(f"SELECT * FROM orders WHERE order_id = {order_id}").fetchmany(1),
#                            reply_markup=price_kb)



#
#
# async def send_order_form(subject_name, order_info: tuple):
#     bot.send_message(text='Новый заказ, детали:\n' + order_info[2],
#                      chat_id=subjects_id[subject_name],
#                      reply_markup=price_keyboard)
