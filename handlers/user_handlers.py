from datetime import datetime
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message, ContentType, BufferedInputFile
from lexicon.lexicon import MESSAGES
from config_data.sessions_config import TYPES
from keyboards.keyboards import generate_calendar, generate_types_duration

router = Router()
session = {}


@router.message(Command(commands='start'))
async def start(message: Message):
    await message.answer(MESSAGES['/start'], parse_mode='HTML')


@router.message(Command(commands='new'))
async def start(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    session[user_id] = {'username': username, 'type': '', 'duration': 3, 'date': '', 'time': ''}
    await message.answer('Select type and duration:', reply_markup=generate_types_duration())
    await message.answer(text=f'Duration: <b>{3}</b> hours.', parse_mode='HTML')


@router.callback_query(F.data.startswith(('confirm_types', *TYPES)))
async def handle_types(callback_query: CallbackQuery):
    action = callback_query.data
    user_id = callback_query.from_user.id

    if action == 'confirm_types':
        await callback_query.answer()
        await callback_query.message.answer(text=f'Choose a day {session}')
        await callback_query.message.edit_reply_markup(reply_markup=generate_calendar())
    elif action in TYPES:
        session[user_id]['type'] = action
        await callback_query.message.answer(text=f'<b>{action}</b> type selected.', parse_mode='HTML')


@router.callback_query(F.data.startswith(('prev', 'next')))
async def handle_nav_calendar(callback_query: CallbackQuery):
    action, year, month = callback_query.data.split('-')
    year = int(year)
    month = int(month)
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


@router.callback_query(F.data == 'choose')
async def handle_choose(callback_query: CallbackQuery):
    data_parts = callback_query.data.split('-')
    year = int(data_parts[1])
    month = int(data_parts[2])
    day = int(data_parts[3])

    chosen_date_message = f"You have chosen the date: {year}-{month:02d}-{day:02d}"
    await callback_query.message.answer(chosen_date_message)
    # await callback_query.message.edit_reply_markup(reply_markup=None)
    # await callback_query.message.edit_reply_markup(reply_markup=generate_calendar(year, month))
