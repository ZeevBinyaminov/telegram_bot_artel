from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from database import sqlite_db
from keyboards import client_kb


async def send_welcome(message: types.Message):
    await message.answer("Привет! Я чат-бот Артель.\nЧем могу помочь?",
                         reply_markup=client_kb.user_inkb)


### check mindmap
class FSMClient(StatesGroup):
    # client branch
    user_status = State()
    is_premium = State()
    subject = State()
    # another_subject = State
    details = State()
    # performer branch
    performer = State()
    subjects = State()
    # other branch
    other = State()
    suggestions = State()
    # finish state


async def cancel_callback(callback: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await callback.message.reply("Нечего отменять")
        await callback.answer()
        return
    await state.finish()
    await callback.message.edit_text(text="Запрос отменен.\nВведите /help, если хотите начать сначала",
                                     reply_markup=None)
    await callback.answer()


async def start_client_fsm(callback: types.CallbackQuery, state: FSMContext):
    await FSMClient.user_status.set()
    async with state.proxy() as data:
        data['user_tag'] = callback.from_user.username


async def become_client(callback: types.CallbackQuery, state: FSMContext):
    await start_client_fsm(callback, state)
    await FSMClient.next()
    await callback.message.edit_text(text='Хотите заказать обычное или премиальное исполнение ?')
    await callback.message.edit_reply_markup(reply_markup=client_kb.is_premium_inkb)


async def is_premium_order(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['is_premium'] = int(callback.data.split()[1])  # change to Bool(True False) if not working
    await FSMClient.next()
    await callback.message.edit_text(text='Выберите предмет')
    await callback.message.edit_reply_markup(reply_markup=client_kb.subjects_inkb)


async def choose_subject(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['subject'] = callback.data
        if data['subject'] != 'Другое':
            await FSMClient.next()
            await callback.message.edit_text(text='Конкретизируйте Ваш заказ (сроки, детали, иные пожелания)')
            await callback.message.edit_reply_markup(reply_markup=types.InlineKeyboardMarkup().add(client_kb.cancel_button))
        else:
            await callback.message.edit_text(text="Введите название предмета")
            await callback.message.edit_reply_markup(reply_markup=types.InlineKeyboardMarkup().add(client_kb.cancel_button))


async def get_another_subject(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['subject'] = message.text
    await FSMClient.next()
    await message.answer(text='Конкретизируйте Ваш заказ (сроки, детали, иные пожелания)',
                         reply_markup=types.InlineKeyboardMarkup().add(client_kb.cancel_button))


async def get_order_details(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['order_details'] = message.text
    await sqlite_db.sql_add_command(state=state, table_name='orders')
    await message.answer(text="Спасибо, мы свяжемся с Вами в ближайшее время!")
    await state.finish()


async def become_performer(callback: types.CallbackQuery, state: FSMContext):
    await start_client_fsm(callback, state)
    await callback.message.answer('Хорошо 2!')
    await callback.answer()


async def become_other(callback: types.CallbackQuery, state: FSMContext):
    await start_client_fsm(callback, state)
    await FSMClient.suggestions.set()
    await callback.message.edit_text(text='Оставьте заявку, и мы свяжемся по Вашему вопросу',
                                     reply_markup=None)

async def get_other_suggestions(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['suggestions'] = message.text
    await sqlite_db.sql_add_command(state=state, table_name='others')
    await message.answer(text="Ожидайте ответа, мы с Вами скоро свяжемся!")
    await state.finish()


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start', 'help'])


def register_callbacks_and_handlers_client(dp: Dispatcher):
    dp.register_callback_query_handler(cancel_callback, state="*", text='cancel')

    dp.register_callback_query_handler(become_client, text='become client', state=None)
    dp.register_callback_query_handler(is_premium_order, Text(startswith='is_premium'),
                                       state=FSMClient.is_premium)
    dp.register_callback_query_handler(choose_subject, state=FSMClient.subject)
    dp.register_message_handler(get_another_subject, state=FSMClient.subject)
    dp.register_message_handler(get_order_details, state=FSMClient.details)

    dp.register_callback_query_handler(become_performer, text='become performer', state=None)
    dp.register_message_handler(get_other_suggestions, state=FSMClient.suggestions)

    dp.register_callback_query_handler(become_other, text='become other', state=None)
