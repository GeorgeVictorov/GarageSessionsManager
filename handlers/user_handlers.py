import re
import calendar
from datetime import datetime
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from lexicon.lexicon import MESSAGES, INFO
from services.services import SessionManager, parse_session_data, format_sessions_info
from keyboards.keyboards import generate_confirm_session, generate_sessions_keyboard
from keyboards.calendar_keyboard import generate_calendar
from keyboards.types_keyboard import generate_types_duration
from keyboards.hours_keyboard import generate_hours_keyboard
from database.sessions_user import book_new_session, upcoming_sessions, cancel_session, change_user_number
from database.sessions_admin import admin_canceled_info
from database.sqlite import update_cached_users
from config_data.sessions_config import TYPES
from config_data.config import load_config
from filters.callback_factory import ChooseDateCallback, ChooseHourCallback, CancelSessionCallback
from middlewares.registration_middleware import RegistrationMiddleware

router = Router()
router.message.middleware(RegistrationMiddleware())
session_manager = SessionManager()


@router.message(Command(commands='start'))
async def start(message: Message):
    await message.answer(MESSAGES['/start'], parse_mode='HTML')


@router.message(Command(commands='new'))
async def new_session(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username

    session_manager.set_session(user_id, {
        'username': username,
        'type': 'Nothing',
        'duration': 3,
        'date': '',
        'time': ''
    })

    await message.answer(text='Choose a date:', reply_markup=generate_calendar())


@router.message(Command(commands='upcoming'))
async def upcoming(message: Message):
    user_id = message.from_user.id
    booked_sessions = upcoming_sessions(user_id)

    if booked_sessions:
        sessions_info = format_sessions_info(booked_sessions)
        response_message = MESSAGES['/upcoming'].format(sessions_info)
    else:
        response_message = MESSAGES['/no_upcoming']

    await message.answer(response_message, parse_mode='HTML')


@router.message(Command(commands='cancel'))
async def cancel(message: Message):
    user_id = message.from_user.id

    keyboard_markup = generate_sessions_keyboard(user_id)

    if keyboard_markup.inline_keyboard:
        response_message = MESSAGES['/cancel']
    else:
        response_message = MESSAGES['/no_upcoming']

    await message.answer(response_message, parse_mode='HTML', reply_markup=keyboard_markup)


@router.callback_query(CancelSessionCallback.filter())
async def cancel_upcoming_sessions(callback_query: CallbackQuery,
                                   callback_data: CancelSessionCallback):
    action, session_id = callback_data.pack().split('-')
    user_id = callback_query.from_user.id
    username = callback_query.from_user.username
    session_start, duration, type_desc = admin_canceled_info(session_id)
    cancel_session(int(session_id))

    await callback_query.message.answer(MESSAGES['/cancel_success'])

    for admin_id in load_config().tg_bot.admin_ids:
        admin_message = INFO['session_admin_cancel'].format(username, session_start, duration, type_desc)
        await callback_query.bot.send_message(admin_id, admin_message, parse_mode='HTML')

    keyboard_markup = generate_sessions_keyboard(user_id)

    if keyboard_markup.inline_keyboard:
        response_message = MESSAGES['/cancel']
    else:
        response_message = MESSAGES['/no_upcoming']

    await callback_query.message.edit_text(response_message, parse_mode='HTML', reply_markup=keyboard_markup)


@router.callback_query(F.data == 'close_user')
async def close_menu(callback_query: CallbackQuery):
    await callback_query.message.edit_text(text=INFO['close'],
                                           parse_mode='HTML')


@router.message(Command(commands='help'))
async def help_message(message: Message):
    await message.answer(MESSAGES['/help'], parse_mode='HTML')


@router.message(Command(commands='change_number'))
async def help_message(message: Message):
    await message.answer(MESSAGES['/change_number'], parse_mode='HTML')


@router.message(Command(commands='change'))
async def change_number(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    command_args = message.text.split()

    if len(command_args) != 2:
        await message.answer(MESSAGES['/change_number_error'], parse_mode='HTML')
        return

    _, phone_number = message.text.split()

    if phone_number is not None:
        if not re.match(r'(?:\+7|8)?[- ]?\(?(9\d{2})\)?[- ]?(\d{3})[- ]?(\d{2})[- ]?(\d{2})', phone_number):
            await message.answer(MESSAGES['/change_number_error'], parse_mode='HTML')
        else:
            if phone_number.startswith('8'):
                phone_number = '+7' + phone_number[1:]

            formatted_phone_number = re.sub(r'^(\+\d)(\d{3})(\d{3})(\d{2})(\d{2})$',
                                            r'\1 (\2) \3-\4-\5',
                                            phone_number)
            user_phone = change_user_number(user_id, formatted_phone_number)
            if user_phone is not None:
                update_cached_users()
                await message.answer(f"Phone number for <b>{username}</b> changed to <b>{phone_number}</b>.",
                                     parse_mode='HTML')
    else:
        await message.answer("An error occurred while changing the number.")


@router.callback_query(F.data.in_({'session', 'return_session', 'cancel_session'}))
async def session_navigation(callback_query: CallbackQuery):
    action = callback_query.data
    user_id = callback_query.from_user.id
    username = callback_query.from_user.username

    if action == 'return_session':
        session_data = session_manager.get_session(user_id)
        session_data['time'] = ''
        session_manager.set_session(user_id, session_data)
        await callback_query.message.edit_text(text=f'Choose time:')
        await callback_query.message.edit_reply_markup(
            reply_markup=generate_hours_keyboard(session_data['date'], session_data['duration']))

    elif action == 'cancel_session':
        session_manager.clear_session(user_id)
        await callback_query.message.edit_text(text=INFO['cancel'], parse_mode='HTML')

    elif action == 'session':
        session_start, session_end, duration, session_type = parse_session_data(session_manager.get_session(user_id))
        db_session_type = TYPES.get(session_type, '')
        book_new_session(user_id, username, session_start, session_end, duration, db_session_type)
        formatted_text = INFO['session_booked'].format(username, session_start, duration, session_type)
        await callback_query.message.edit_text(text=formatted_text, parse_mode='HTML')
        session_manager.clear_session(user_id)

        admin_ids = load_config().tg_bot.admin_ids
        for admin_id in admin_ids:
            admin_message = INFO['session_admin_info'].format(username, session_start, duration, session_type)
            await callback_query.bot.send_message(admin_id, admin_message, parse_mode='HTML')


@router.callback_query(F.data.in_({'confirm_session', 'back_to_types'}))
async def hours_navigation(callback_query: CallbackQuery):
    action = callback_query.data
    user_id = callback_query.from_user.id
    username = callback_query.from_user.username

    if action == 'confirm_session' and session_manager.get_session(user_id)['time']:
        session_date, _, duration, session_type = parse_session_data(session_manager.get_session(user_id))
        formatted_text = INFO['session'].format(username, session_date, duration, session_type)
        await callback_query.message.edit_text(
            text=formatted_text, parse_mode='HTML')
        await callback_query.message.edit_reply_markup(reply_markup=generate_confirm_session())

    elif action == 'back_to_types':
        session_data = session_manager.get_session(user_id)
        session_data['duration'] = 3
        session_data['type'] = 'no type'
        session_manager.set_session(user_id, session_data)
        await callback_query.message.edit_text(text='Choose type and duration:',
                                               reply_markup=generate_types_duration())


@router.callback_query(ChooseHourCallback.filter())
async def hours_choose(callback_query: CallbackQuery,
                       callback_data: ChooseHourCallback):
    action, hour = callback_data.pack().split('-')
    user_id = callback_query.from_user.id

    session_data = session_manager.get_session(user_id)
    if hour != session_data['time']:
        session_data['time'] = hour
        chosen_hour_message = f"Start time: <b>{hour.split(':')[0]}:{hour.split(':')[1]}</b>"
        session_manager.set_session(user_id, session_data)
        await callback_query.message.edit_text(chosen_hour_message, parse_mode='HTML',
                                               reply_markup=generate_hours_keyboard(session_data['date'],
                                                                                    session_data['duration']))


@router.callback_query(F.data.in_({'confirm_types', 'return_types', *TYPES}))
async def types_navigation(callback_query: CallbackQuery):
    action = callback_query.data
    user_id = callback_query.from_user.id

    session_data = session_manager.get_session(user_id)
    if action == 'confirm_types' and session_data['type'] and session_data['type'] != 'Nothing':
        await callback_query.message.edit_text(text=f'Choose time:')
        await callback_query.message.edit_reply_markup(
            reply_markup=generate_hours_keyboard(session_data['date'], session_data['duration']))
    elif action == 'return_types':
        session_data['date'] = ''
        session_data['type'] = 'no type'
        session_manager.set_session(user_id, session_data)
        await callback_query.message.edit_text(text='Choose a date:', reply_markup=generate_calendar())
    elif action in TYPES:
        if action != session_data['type']:
            session_data['type'] = action
            hour = session_data['duration']
            session_manager.set_session(user_id, session_data)
            await callback_query.message.edit_text(text=f'<b>{action}</b> selected. <b>{hour}</b> hours.',
                                                   parse_mode='HTML',
                                                   reply_markup=generate_types_duration(hour))


@router.callback_query(F.data.startswith(('less', 'more')))
async def types_duration(callback_query: CallbackQuery):
    action, hour = callback_query.data.split('-')
    user_id = callback_query.from_user.id
    hour = int(hour)

    session_data = session_manager.get_session(user_id)
    if action == 'less' and hour > 1:
        hour -= 1
    elif action == 'more':
        hour += 1
    session_data['duration'] = hour
    session_manager.set_session(user_id, session_data)
    session_type = session_data['type']
    await callback_query.message.edit_text(text=f'<b>{session_type}</b> selected. <b>{hour}</b> hours.',
                                           parse_mode='HTML',
                                           reply_markup=generate_types_duration(hour, disable_less=hour == 1))


@router.callback_query(F.data.startswith(('prev', 'next')))
async def calendar_navigation(callback_query: CallbackQuery):
    action, year, month = callback_query.data.split('-')
    year, month = int(year), int(month)
    if action == 'prev':
        month -= 1
        if month == 0:
            year -= 1
            month = 12
    elif action == 'next':
        month += 1
        if month == 13:
            year += 1
            month = 1
    await callback_query.message.edit_reply_markup(reply_markup=generate_calendar(year, month))


@router.callback_query(F.data == 'confirm_calendar')
async def calendar_confirm(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    session_data = session_manager.get_session(user_id)

    if session_data['date']:
        year, month, day = map(int, session_data['date'].split('-'))
        session_date = datetime(year, month, day)
        current_date = datetime.now().date()

        if session_date.date() >= current_date:
            await callback_query.message.edit_text(text='Choose type and duration:',
                                                   reply_markup=generate_types_duration())


@router.callback_query(ChooseDateCallback.filter())
async def calendar_choose(callback_query: CallbackQuery,
                          callback_data: ChooseDateCallback):
    year, month, day = map(int, callback_data.pack().split('-')[1:])

    user_id = callback_query.from_user.id
    chosen_date = f'{year}-{month}-{day}'

    if chosen_date:
        year, month, day = map(int, chosen_date.split('-'))
        session_date = datetime(year, month, day)
        current_date = datetime.now().date()

        session_data = session_manager.get_session(user_id)
        if chosen_date != session_data['date'] and session_date.date() >= current_date:
            session_data['date'] = chosen_date
            session_manager.set_session(user_id, session_data)
            chosen_date_message = f"Date: <b>{day:02d}</b> {calendar.month_name[month]}."
            await callback_query.message.edit_text(chosen_date_message, parse_mode='HTML',
                                                   reply_markup=generate_calendar(year, month))
