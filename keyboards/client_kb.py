from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


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
user_inkb.add(become_client, become_performer, become_other, cancel_button)

subjects_inkb = InlineKeyboardMarkup(row_width=2)
subjects_list = ['Математика', 'История', 'Социология',
                 'Политология', 'Международные отношения',
                 'Право', 'Государственное управление',
                 'Урабанистика', 'Философия', 'Филология',
                 'Экономика', 'Программирование', 'Другое']
for subject in subjects_list:
    subjects_inkb.insert(InlineKeyboardButton(text=subject, callback_data=subject))
subjects_inkb.add(cancel_button)
