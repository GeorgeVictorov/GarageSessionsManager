from datetime import datetime
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message, ContentType, BufferedInputFile
from lexicon.lexicon import MESSAGES
from keyboards.keyboards import generate_calendar

router = Router()


@router.message(Command(commands='start'))
async def start(message: Message):
    current_date = datetime.now()
    await message.answer('Select a date:', reply_markup=generate_calendar())


@router.callback_query(F.data.startswith(('prev', 'next')))
async def handle_nav_buttons(callback_query: CallbackQuery):
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


@router.callback_query(F.data.startswith('choose'))
async def handle_choose(callback_query: CallbackQuery):
    data_parts = callback_query.data.split('-')
    year = int(data_parts[1])
    month = int(data_parts[2])
    day = int(data_parts[3])

    chosen_date_message = f"You have chosen the date: {year}-{month:02d}-{day:02d}"
    await callback_query.message.answer(chosen_date_message)
    await callback_query.message.edit_reply_markup(reply_markup=None)
    # await callback_query.message.edit_reply_markup(reply_markup=generate_calendar(year, month))
