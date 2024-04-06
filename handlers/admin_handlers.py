from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from keyboards.keyboards import generate_admin_sessions
from lexicon.lexicon import MESSAGES, INFO
from database.sessions_admin import admin_upcoming_sessions, admin_cancel_session, admin_canceled_info
from services.admin import format_sessions
from filters.admin import IsAdmin
from filters.callback_factory import AdminCancelCallback
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
async def admin_start(message: Message):
    keyboard_markup = generate_admin_sessions()

    if keyboard_markup.inline_keyboard:
        response_message = MESSAGES['/admin_cancel']
    else:
        response_message = MESSAGES['/admin_no_upcoming']

    await message.answer(response_message, parse_mode='HTML', reply_markup=keyboard_markup)


@router.callback_query(AdminCancelCallback.filter(), IsAdmin())
async def cancel_upcoming_sessions(callback_query: CallbackQuery,
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


@router.callback_query(F.data == 'admin_close_cancel', IsAdmin())
async def close_cancel_upcoming_sessions(callback_query: CallbackQuery):
    await callback_query.message.edit_text(text=INFO['close'],
                                           parse_mode='HTML')
