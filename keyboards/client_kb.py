from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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

is_premium_inkb = InlineKeyboardMarkup(row_width=2)
yes_button = InlineKeyboardButton(text='Премиальное', callback_data='is_premium 1')
no_button = InlineKeyboardButton(text='Обычное', callback_data='is_premium 0')
is_premium_inkb.add(yes_button, no_button, cancel_button)