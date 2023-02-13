import re

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from database import sqlite_db
from keyboards import client_kb
from loader import bot


async def send_welcome(message: types.Message):
    await bot.send_message(
        text="Привет! Я чат-бот Артель",
        chat_id=message.from_user.id,
        reply_markup=client_kb.ReplyKeyboardRemove()
    )
    await message.answer(
        text="Чем могу помочь?",
        reply_markup=client_kb.user_inkb
    )


async def send_help(message: types.Message):
    await bot.send_message(
        text="Привет! Я чат-бот Артель",
        chat_id=message.from_user.id,
        reply_markup=client_kb.ReplyKeyboardRemove()
    )
    await message.answer("Чем могу помочь?",
                         reply_markup=client_kb.user_inkb)


phone_pat = re.compile(r"(\d\s*){11}")
link_pat = re.compile(r"(https://(www.)?)?(instagram|vk|t).(com|me).*")
tag_pat = re.compile(r"@.+")
words_pat = re.compile(r"\b(тг|tg|вк|vk|vkontakte|инстаграмм|инст(а|ы|ой|у|е)?|inst)\b")


def is_allowed_message(text):
    phone_match = re.match(string=text, pattern=phone_pat)
    link_match = re.match(string=text, pattern=link_pat)
    tag_match = re.match(string=text, pattern=tag_pat)
    words_match = re.match(string=text, pattern=words_pat)
    return not (phone_match or link_match or tag_match or words_match)


async def send_message(message: types.Message):
    if message.chat.type == "private":
        chat_id = sqlite_db.get_active_chat(message.from_user.id)
        if chat_id:
            if message.content_type == 'text' and is_allowed_message(message.text):
                await bot.send_message(text=message.text, chat_id=chat_id)
            if message.content_type == 'document':
                await bot.send_document(document=message.document.file_id, chat_id=chat_id)


class FSMClient(StatesGroup):
    # client branch
    user_status = State()
    client_subject = State()
    client_details = State()
    # performer branch
    performer_subject = State()
    performer_experience = State()
    # other branch
    suggestions = State()
    # finish state


class FSMOrder(StatesGroup):
    get_price = State()


async def cancel_callback(callback: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await callback.message.reply("Нечего отменять")
        await callback.answer()
        return
    await state.finish()
    await callback.message.edit_text(text="Запрос отменен.",
                                     reply_markup=None)
    await callback.message.answer(text='Хотите начать сначала ?',
                                  reply_markup=client_kb.main_menu)
    await callback.answer()


async def start_client_fsm(callback: types.CallbackQuery, state: FSMContext):
    await FSMClient.user_status.set()
    async with state.proxy() as data:
        data['user_tag'] = callback.from_user.username


# client
async def become_client(callback: types.CallbackQuery, state: FSMContext):
    await start_client_fsm(callback, state)
    await FSMClient.next()
    await callback.message.edit_text(text='Выберите предмет')
    await callback.message.edit_reply_markup(reply_markup=client_kb.subjects_inkb)


async def choose_client_subject(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['subject'] = callback.data
        if data['subject'] != 'Другое (укажите Ваш предмет)':
            await FSMClient.next()
            await callback.message.edit_text(text='Конкретизируйте Ваш заказ (сроки, детали, иные пожелания)')
            await callback.message.edit_reply_markup(reply_markup=client_kb.cancel_inkb)
        else:
            await callback.message.edit_text(text="Введите название предмета")
            await callback.message.edit_reply_markup(reply_markup=client_kb.cancel_inkb)


async def get_another_subject(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['subject'] = message.text
    await FSMClient.next()
    await message.answer(text='Конкретизируйте Ваш заказ (сроки, детали, иные пожелания)'
                              '\nЕсли у Вас есть промокод, можете ввести его в это поле вместе с доп. информацией',
                         reply_markup=client_kb.cancel_inkb)


async def get_order_details(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        order_id = message.from_user.id * 2
        subject_id = client_kb.subjects_dict[data['subject']]
        data['order_details'] = message.text
        data['order_id'] = order_id // 2
        message_id = (await bot.send_message(chat_id=subject_id,
                                             text=data['order_details'] + f"\n{order_id}",
                                             reply_markup=client_kb.reply_inkb)).message_id
        data['message_id'] = message_id

    await sqlite_db.sql_add_command(state=state, table_name='orders')

    await message.answer(text="Спасибо, мы свяжемся с Вами в ближайшее время!",
                         reply_markup=client_kb.main_menu)
    await state.finish()


# offer price
async def reply_to_order(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    info = sqlite_db.sql_select("SELECT is_busy "
                                "FROM performers "
                                "WHERE performer_id = ?", (user_id,))
    if not info:
        await callback.bot.send_message(text="Вы не являетесь исполнителем",
                                        chat_id=user_id)
        await callback.answer()
        return

    is_busy = info[0][0]
    if is_busy:
        await callback.bot.send_message(text="У Вас есть текущий заказ",
                                        chat_id=user_id)
        return
    await callback.bot.send_message(text=callback.message.text,
                                    reply_markup=client_kb.price_inkb,
                                    chat_id=user_id)


async def ask_price(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    await FSMOrder.get_price.set()
    async with state.proxy() as data:
        message_text = callback.message.text.split("\n")
        order_id = int(message_text[-1])
        data['order_id'] = order_id // 2
        data['performer_id'] = callback.from_user.id
        await callback.bot.send_message(text=f"Введите свою цену: {order_id}", chat_id=callback.from_user.id)


async def get_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        price = message.text
        if not price.isnumeric():
            await message.answer("Неправильный формат цены, введите еще раз")
            return
        price = int(price)
        price_res = price * 1.25
        data['price'] = price_res
        await message.answer(text=f"Ваша цена записана: {price}")

        description = sqlite_db.sql_select("SELECT description "
                                           "FROM perf_description "
                                           "WHERE performer_id = ?", (data['performer_id'],))[0][0]
        text = f"{data['performer_id'] * 2}: {description}\nЦена: {price_res:.0f}"
        await client_kb.send_performer_suggestion(client_id=data['order_id'],
                                                  text=text)
    await state.finish()


async def accept_price(callback: types.CallbackQuery):
    performer_id = int(callback.message.text.split(":")[0]) // 2
    order_id = callback.from_user.id

    # edit message in a subject chat
    subject, message_id, details = sqlite_db.sql_select("SELECT subject, message_id, order_details "
                                                        "FROM orders "
                                                        "WHERE order_id = ?", (order_id,))[0]

    subject_id = client_kb.subjects_dict[subject]
    await bot.edit_message_text(chat_id=subject_id,
                                message_id=message_id,
                                text=f"{details} (в процессе)")

    sqlite_db.sql_execute("UPDATE performers "
                          "SET is_busy = 1 "
                          "WHERE performer_id = ?", (performer_id,))
    # create chat
    sqlite_db.sql_execute("DELETE FROM orders "
                          "WHERE order_id = ?", (order_id,))

    sqlite_db.sql_execute("INSERT INTO chats (chat_one, chat_two)"
                          "VALUES (?, ?)", (order_id, performer_id,))

    # send notification to admins and client and performer like
    await bot.send_message(chat_id=performer_id,
                           text=f"Вы получили заказ:\n{details}.",
                           reply_markup=client_kb.ReplyKeyboardRemove())
    await bot.send_message(chat_id=performer_id,
                           text="Чат с заказчиком открыт",
                           reply_markup=client_kb.close_chat_kb)  # cancel_order_inkb)

    await callback.message.edit_reply_markup()
    await callback.message.answer(text="Пожалуйста, оплатите 50% от суммы по номеру (номер)\n"
                                       "Переносим Вас в чат с исполнителем",
                                  reply_markup=client_kb.close_chat_kb)  # cancel_order_inkb)


async def deny_price(callback: types.CallbackQuery):
    await callback.message.edit_text(text="Ожидайте следующих заявок от исполнителей",
                                     reply_markup=None)


async def close_chat(message: types.Message):
    chat_id = sqlite_db.get_active_chat(message.from_user.id)
    # await message.edit_reply_markup()
    await message.answer(text="Чат закрыт", reply_markup=client_kb.ReplyKeyboardRemove())
    await bot.send_message(chat_id=chat_id, text="Чат закрыт", reply_markup=client_kb.ReplyKeyboardRemove())

    sqlite_db.sql_execute("DELETE FROM chats "
                          "WHERE chat_one = ? OR chat_two = ?", (chat_id, chat_id))

    sqlite_db.sql_execute("UPDATE performers "
                          "SET is_busy = 0 "
                          "WHERE performer_id = ? OR performer_id = ?", (chat_id, message.from_user.id,))


# performer
async def become_performer(callback: types.CallbackQuery, state: FSMContext):
    await start_client_fsm(callback, state)
    await FSMClient.performer_subject.set()
    await callback.message.edit_text(text='Выберите предмет')
    await callback.message.edit_reply_markup(reply_markup=client_kb.subjects_inkb)


async def choose_performer_subject(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['performer_id'] = callback.from_user.id
        data['subject'] = callback.data
    await FSMClient.performer_experience.set()
    await callback.message.edit_text("Опишите свой опыт и навыки", reply_markup=client_kb.cancel_inkb)


async def get_performer_details(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['performer_details'] = message.text
    await sqlite_db.sql_add_command(state=state, table_name='performers')
    await state.finish()
    await message.answer(text="Ожидайте ответа, мы с Вами скоро свяжемся!",
                         reply_markup=client_kb.main_menu)


# other
async def become_other(callback: types.CallbackQuery, state: FSMContext):
    await start_client_fsm(callback, state)
    await FSMClient.suggestions.set()
    await callback.message.edit_text(text='Оставьте заявку, и мы свяжемся по Вашему вопросу',
                                     reply_markup=client_kb.cancel_inkb)


async def get_another_suggestions(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['suggestions'] = message.text
    await sqlite_db.sql_add_command(state=state, table_name='others')
    await message.answer(text="Ожидайте ответа, мы с Вами скоро свяжемся!",
                         reply_markup=client_kb.main_menu)
    await state.finish()


def register_callbacks_and_handlers_client(dp: Dispatcher):
    dp.register_callback_query_handler(cancel_callback, state="*", text='cancel')
    dp.register_message_handler(send_welcome, commands=['start'])
    dp.register_message_handler(send_help, commands=['help'])
    dp.register_message_handler(close_chat, commands=['Закрыть_чат'])
    dp.register_message_handler(send_message, content_types=['text', 'document'])

    dp.register_callback_query_handler(become_client, text='become client', state=None)
    dp.register_callback_query_handler(choose_client_subject, state=FSMClient.client_subject)
    dp.register_message_handler(get_another_subject, state=FSMClient.client_subject)
    dp.register_message_handler(get_order_details, state=FSMClient.client_details)

    dp.register_callback_query_handler(reply_to_order, text='reply')
    dp.register_callback_query_handler(ask_price, text="ask price", state=None)
    dp.register_message_handler(get_price, state=FSMOrder.get_price)

    dp.register_callback_query_handler(accept_price, text='accept price')
    dp.register_callback_query_handler(deny_price, text='deny price')

    dp.register_callback_query_handler(become_performer, text='become performer', state=None)
    dp.register_callback_query_handler(choose_performer_subject, state=FSMClient.performer_subject)
    dp.register_message_handler(get_performer_details, state=FSMClient.performer_experience)

    dp.register_callback_query_handler(become_other, text='become other', state=None)
    dp.register_message_handler(get_another_suggestions, state=FSMClient.suggestions)
