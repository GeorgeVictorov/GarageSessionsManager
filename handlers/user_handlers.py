import calendar
from datetime import datetime
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message, ContentType, BufferedInputFile
from lexicon.lexicon import MESSAGES
from config_data.sessions_config import TYPES
from keyboards.keyboards import generate_calendar, generate_types_duration, generate_hours_keyboard, \
    generate_confirm_session

router = Router()
session = {}


# def parse_session_data(session: dict, user_id: int):
#     session_date = f'{session[user_id]["date"]} {session[user_id]["time"]}'
#     session_date = datetime.strptime(session_date, '%Y-%m-%d %H:%M:%S')
#     duration = session[user_id]['duration']
#     session_type = session[user_id]['type']
#     return session_date, duration, session_type


@router.message(Command(commands='start'))
async def start(message: Message):
    await message.answer(MESSAGES['/start'], parse_mode='HTML')


@router.message(Command(commands='new'))
async def start(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username

    session[user_id] = {
        'username': username,
        'type': 'Nothing',
        'duration': 3,
        'date': '',
        'time': ''
    }

    await message.answer(text='Choose a date:', reply_markup=generate_calendar())


@router.callback_query(F.data.in_({'confirm_session', 'back_to_types'}))
async def hours_navigation(callback_query: CallbackQuery):
    action = callback_query.data
    user_id = callback_query.from_user.id
    username = callback_query.from_user.username

    if action == 'confirm_session' and session[user_id]['time']:
        session_date = f'{session[user_id]['date']} {session[user_id]['time']}'
        session_date = datetime.strptime(session_date, '%Y-%m-%d %H:%M:%S')
        duration = session[user_id]['duration']
        session_type = session[user_id]['type']
        await callback_query.message.edit_text(
            text=f'New session for <b>{username}</b>'
                 f'\n\nStart time: <b>{session_date}</b>'
                 f'\n\nFor <b>{duration}</b> hours, type <b>{session_type}</b>', parse_mode='HTML')
        await callback_query.message.edit_reply_markup(reply_markup=generate_confirm_session())

    elif action == 'back_to_types':
        session[user_id]['time'] = ''
        session[user_id]['type'] = 'Nothing'
        await callback_query.message.edit_text(text='Choose time:',
                                               reply_markup=generate_types_duration())


@router.callback_query(F.data.startswith('hour'))
async def hours_choose(callback_query: CallbackQuery):
    action, hour = callback_query.data.split('-')
    user_id = callback_query.from_user.id

    if hour != session[user_id]['time']:
        session[user_id]['time'] = hour
        chosen_hour_message = f"Start time: <b>{hour.split(':')[0]}:{hour.split(':')[1]}</b>"
        await callback_query.message.edit_text(chosen_hour_message, parse_mode='HTML',
                                               reply_markup=generate_hours_keyboard(session[user_id]['date'],
                                                                                    session[user_id]['duration']))


@router.callback_query(F.data.in_({'confirm_types', 'return_types', *TYPES}))
async def types_navigation(callback_query: CallbackQuery):
    action = callback_query.data
    user_id = callback_query.from_user.id

    if action == 'confirm_types' and session[user_id]['type'] and session[user_id]['type'] != 'Nothing':
        await callback_query.message.edit_text(text=f'Choose time:')
        await callback_query.message.edit_reply_markup(
            reply_markup=generate_hours_keyboard(session[user_id]['date'], session[user_id]['duration']))
    elif action == 'return_types':
        session[user_id]['date'] = ''
        session[user_id]['type'] = 'Nothing'
        await callback_query.message.edit_text(text='Choose a date:', reply_markup=generate_calendar())
    elif action in TYPES:
        if action != session[user_id]['type']:
            session[user_id]['type'] = action
            hour = session[user_id]['duration']
            await callback_query.message.edit_text(text=f'<b>{action}</b> selected. <b>{hour}</b> hours.',
                                                   parse_mode='HTML',
                                                   reply_markup=generate_types_duration(hour))


@router.callback_query(F.data.startswith(('less', 'more')))
async def types_duration(callback_query: CallbackQuery):
    action, hour = callback_query.data.split('-')
    user_id = callback_query.from_user.id
    hour = int(hour)

    if action == 'less' and hour > 1:
        hour -= 1
        session[user_id]['duration'] = hour
    elif action == 'more':
        hour += 1
        session[user_id]['duration'] = hour

    session_type = session[user_id]['type']
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
    if session[user_id]['date']:
        await callback_query.message.edit_text(text='Choose type and duration:', reply_markup=generate_types_duration())


@router.callback_query(F.data.startswith('choose'))
async def calendar_choose(callback_query: CallbackQuery):
    data_parts = callback_query.data.split('-')
    year, month, day = map(int, data_parts[1:])

    user_id = callback_query.from_user.id
    chosen_date = f'{year}-{month}-{day}'

    if chosen_date != session[user_id]['date']:
        session[user_id]['date'] = chosen_date
        chosen_date_message = f"Date: <b>{day:02d}</b> {calendar.month_name[month]}."
        await callback_query.message.edit_text(chosen_date_message, parse_mode='HTML',
                                               reply_markup=generate_calendar(year, month))
