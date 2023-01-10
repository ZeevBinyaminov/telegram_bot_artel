from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from database import sqlite_db
from keyboards import client_kb
from keyboards.client_kb import main_menu


async def send_welcome(message: types.Message):
    await message.answer("Привет! Я чат-бот Артель.\nЧем могу помочь?",
                         reply_markup=client_kb.user_inkb)


async def send_help(message: types.Message):
    await message.answer("Чем могу помочь?",
                         reply_markup=client_kb.user_inkb)


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
            await callback.message.edit_reply_markup(
                reply_markup=client_kb.cancel_inkb)
        else:
            await callback.message.edit_text(text="Введите название предмета")
            await callback.message.edit_reply_markup(
                reply_markup=client_kb.cancel_inkb)


async def get_another_subject(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['subject'] = message.text
    await FSMClient.next()
    await message.answer(text='Конкретизируйте Ваш заказ (сроки, детали, иные пожелания)',
                         reply_markup=client_kb.cancel_inkb)


async def get_order_details(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['order_details'] = message.text
    await sqlite_db.sql_add_command(state=state, table_name='orders')
    await message.answer(text="Спасибо, мы свяжемся с Вами в ближайшее время!",
                         reply_markup=main_menu)
    await state.finish()


# performer
async def become_performer(callback: types.CallbackQuery, state: FSMContext):
    await start_client_fsm(callback, state)
    await FSMClient.performer_subject.set()
    await callback.message.edit_text(text='Выберите предмет')
    await callback.message.edit_reply_markup(reply_markup=client_kb.subjects_inkb)


async def choose_performer_subject(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['subject'] = callback.data
    await FSMClient.performer_experience.set()
    await callback.message.edit_text("Опишите свой опыт и навыки", reply_markup=client_kb.cancel_inkb)


async def get_performer_details(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['details'] = message.text
    await sqlite_db.sql_add_command(state=state, table_name='performers')
    await state.finish()
    await message.answer(text="Ожидайте ответа, мы с Вами скоро свяжемся!",
                         reply_markup=main_menu)


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
                         reply_markup=main_menu)
    await state.finish()


def register_callbacks_and_handlers_client(dp: Dispatcher):
    dp.register_callback_query_handler(cancel_callback, state="*", text='cancel')
    dp.register_message_handler(send_welcome, commands=['start'])
    dp.register_message_handler(send_help, commands=['help'])

    dp.register_callback_query_handler(become_client, text='become client', state=None)
    dp.register_callback_query_handler(choose_client_subject, state=FSMClient.client_subject)
    dp.register_message_handler(get_another_subject, state=FSMClient.client_subject)
    dp.register_message_handler(get_order_details, state=FSMClient.client_details)

    dp.register_callback_query_handler(become_performer, text='become performer', state=None)
    dp.register_callback_query_handler(choose_performer_subject, state=FSMClient.performer_subject)
    dp.register_message_handler(get_performer_details, state=FSMClient.performer_experience)

    dp.register_callback_query_handler(become_other, text='become other', state=None)
    dp.register_message_handler(get_another_suggestions, state=FSMClient.suggestions)
