import calendar
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from lexicon.lexicon import MESSAGES
from config_data.sessions_config import TYPES
from services.services import SessionManager, parse_session_data
from keyboards.keyboards import generate_calendar, generate_types_duration, generate_hours_keyboard, \
    generate_confirm_session

router = Router()
session = {}
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


@router.callback_query(F.data.in_({'confirm_session', 'back_to_types'}))
async def hours_navigation(callback_query: CallbackQuery):
    action = callback_query.data
    user_id = callback_query.from_user.id
    username = callback_query.from_user.username

    if action == 'confirm_session' and session_manager.get_session(user_id)['time']:
        session_date, duration, session_type = parse_session_data(session_manager.get_session(user_id))
        formatted_text = (f"New session for <b>{username}</b>"
                          f"\n\nSession Date: <b>{session_date}</b>"
                          f"\nDuration: <b>{duration} hours</b>"
                          f"\nSession Type: <b>{session_type}</b>")
        await callback_query.message.edit_text(
            text=formatted_text, parse_mode='HTML')
        await callback_query.message.edit_reply_markup(reply_markup=generate_confirm_session())

    elif action == 'back_to_types':
        session_data = session_manager.get_session(user_id)
        session_data['time'] = ''
        session_data['type'] = 'Nothing'
        session_manager.set_session(user_id, session_data)
        await callback_query.message.edit_text(text='Choose time:',
                                               reply_markup=generate_types_duration())


@router.callback_query(F.data.startswith('hour'))
async def hours_choose(callback_query: CallbackQuery):
    action, hour = callback_query.data.split('-')
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
        session_data['type'] = 'Nothing'
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
        await callback_query.message.edit_text(text='Choose type and duration:', reply_markup=generate_types_duration())


@router.callback_query(F.data.startswith('choose'))
async def calendar_choose(callback_query: CallbackQuery):
    data_parts = callback_query.data.split('-')
    year, month, day = map(int, data_parts[1:])

    user_id = callback_query.from_user.id
    chosen_date = f'{year}-{month}-{day}'

    session_data = session_manager.get_session(user_id)
    if chosen_date != session_data['date']:
        session_data['date'] = chosen_date
        session_manager.set_session(user_id, session_data)
        chosen_date_message = f"Date: <b>{day:02d}</b> {calendar.month_name[month]}."
        await callback_query.message.edit_text(chosen_date_message, parse_mode='HTML',
                                               reply_markup=generate_calendar(year, month))
