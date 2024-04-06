from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message, BufferedInputFile
from keyboards.keyboards import generate_admin_sessions, generate_admin_unpaid_sessions
from lexicon.lexicon import MESSAGES, INFO
from database.sessions_admin import admin_upcoming_sessions, admin_cancel_session, admin_canceled_info, \
    admin_confirm_session_payment, update_types_price
from database.select_sessions_data import get_sessions_history, history_to_csv, generate_filename
from services.admin import format_sessions
from filters.admin import IsAdmin
from filters.callback_factory import AdminCancelCallback, AdminPaymentCallback
from config_data.config import load_config

router = Router()


@router.message(Command(commands='admin'), IsAdmin())
async def admin_start(message: Message):
    username = message.from_user.username
    await message.answer(MESSAGES['/admin'].format(username), parse_mode='HTML')


@router.message(Command(commands='admin_upcoming'), IsAdmin())
async def admin_upcoming(message: Message):
    booked_sessions = admin_upcoming_sessions()
    response_message = format_sessions(booked_sessions)
    await message.answer(response_message, parse_mode='HTML')


@router.message(Command(commands='admin_cancel'), IsAdmin())
async def admin_cancel(message: Message):
    keyboard_markup = generate_admin_sessions()

    if keyboard_markup.inline_keyboard:
        response_message = MESSAGES['/admin_cancel']
    else:
        response_message = MESSAGES['/admin_no_upcoming']

    await message.answer(response_message, parse_mode='HTML', reply_markup=keyboard_markup)


@router.callback_query(AdminCancelCallback.filter(), IsAdmin())
async def admin_cancel_upcoming_sessions(callback_query: CallbackQuery,
                                         callback_data: AdminCancelCallback):
    action, session_id = callback_data.pack().split('-')
    username = callback_query.from_user.username
    session_start, duration, type_desc = admin_canceled_info(session_id)

    admin_cancel_session(int(session_id))

    keyboard_markup = generate_admin_sessions()

    for admin_id in load_config().tg_bot.admin_ids:
        admin_message = INFO['session_admin_cancel'].format(username, session_start, duration, type_desc)
        await callback_query.bot.send_message(admin_id, admin_message, parse_mode='HTML')

    if keyboard_markup.inline_keyboard:
        response_message = MESSAGES['/admin_cancel']
    else:
        response_message = MESSAGES['/admin_no_upcoming']

    await callback_query.message.edit_text(response_message, parse_mode='HTML', reply_markup=keyboard_markup)


@router.callback_query(F.data == 'admin_close', IsAdmin())
async def close_admin_cancel_upcoming_sessions(callback_query: CallbackQuery):
    await callback_query.message.edit_text(text=INFO['close'],
                                           parse_mode='HTML')


@router.message(Command(commands='admin_payment'), IsAdmin())
async def admin_payment(message: Message):
    keyboard_markup = generate_admin_unpaid_sessions()

    if keyboard_markup.inline_keyboard:
        response_message = MESSAGES['/admin_payment']
    else:
        response_message = MESSAGES['/admin_no_payment']

    await message.answer(response_message, parse_mode='HTML', reply_markup=keyboard_markup)


@router.callback_query(AdminPaymentCallback.filter(), IsAdmin())
async def admin_confirm_payment(callback_query: CallbackQuery,
                                callback_data: AdminPaymentCallback):
    action, session_id = callback_data.pack().split('-')
    username = callback_query.from_user.username
    session_start, duration, type_desc = admin_canceled_info(session_id)

    admin_confirm_session_payment(int(session_id))

    keyboard_markup = generate_admin_unpaid_sessions()

    for admin_id in load_config().tg_bot.admin_ids:
        admin_message = INFO['session_admin_payment'].format(username, session_start, duration, type_desc)
        await callback_query.bot.send_message(admin_id, admin_message, parse_mode='HTML')

    if keyboard_markup.inline_keyboard:
        response_message = MESSAGES['/admin_payment']
    else:
        response_message = MESSAGES['/admin_no_payment']

    await callback_query.message.edit_text(response_message, parse_mode='HTML', reply_markup=keyboard_markup)


@router.message(Command(commands='admin_sessions'), IsAdmin())
async def send_stats(message: Message):
    cols, rows = get_sessions_history()
    if cols:
        csv_data = history_to_csv(cols, rows)
        file_name = generate_filename(rows)
        await message.answer(text=MESSAGES['/admin_sessions'], parse_mode='HTML')
        await message.answer_document(BufferedInputFile(csv_data.encode(), filename=file_name))


@router.message(Command('admin_update_price'), IsAdmin())
async def update_price(message: Message):
    await message.answer(MESSAGES['/admin_update_price'], parse_mode='HTML')


@router.message(Command(commands='update_price'), IsAdmin())
async def confirm_update_price(message: Message):
    command_args = message.text.split()

    if len(command_args) != 3:
        await message.answer(MESSAGES['/admin_update_price_error'])
        return

    _, type_id, new_price = message.text.split()
    type_desc = await update_types_price(type_id, new_price)
    if type_desc is not None:
        await message.answer(f"Price for type: <b>{type_desc}</b> updated to <b>{new_price}</b>.", parse_mode='HTML')
    else:
        await message.answer("An error occurred while updating price. Please try again later.")
