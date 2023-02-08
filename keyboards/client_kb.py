from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from loader import bot

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
    "проверка": -1001674582859,
    # "Юриспруденция": -1001790959600,
    # "Экономика": -1001852643314,
    # "Политология": -1001679302522,
    # "Социология": -1001608456987,
    # "История": -1001804798141,
    # "Философия": -1001806183269,
    # "Психология": -1001631922451,
    # "Программирование": -1001590590211,
    # "Лингвистика и иностранные языки": -1001862273326,
    # "Математика": -1001763954483,
    # "Филология и литература": -1001823585368,
    # "Искусство": -1001711068367,
    # "Государственное управление": -1001881088844,
    # "Международные отношения": -1001874994032,
    # "Архитектура и урбанистика": -1001854906965,
    # "Маркетинг и бизнес": -1001808316216,
    # "Реклама и журналистика": -1001664717218,
    # "Финансы, аудит и бухучет": -1001804298079,
    # "Биология и медицина": -1001866691571,
    # "Физика": -1001895191555,
    # "Транскрипты": -1001810132774
}

subjects_inkb = InlineKeyboardMarkup(row_width=2)
for subject in subjects_dict:
    subjects_inkb.insert(InlineKeyboardButton(text=subject, callback_data=subject))
subjects_inkb.add(cancel_button)

price_button = InlineKeyboardButton(text="Предложить цену", callback_data="ask price")
price_inkb = InlineKeyboardMarkup(row_width=1)
price_inkb.add(price_button)

reply_button = InlineKeyboardButton(text="Откликнуться", callback_data="reply")
reply_inkb = InlineKeyboardMarkup()
reply_inkb.add(reply_button)


async def send_performer_suggestion(client_id, text):
    accept_button = InlineKeyboardButton(text=f"Принять", callback_data="accept price")
    deny_button = InlineKeyboardButton(text=f"Отклонить", callback_data="deny price")
    suggestion_inkb = InlineKeyboardMarkup()
    suggestion_inkb.add(accept_button, deny_button)
    await bot.send_message(text=text, reply_markup=suggestion_inkb, chat_id=client_id)
