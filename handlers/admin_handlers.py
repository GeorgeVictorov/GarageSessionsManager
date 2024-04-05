from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from lexicon.lexicon import MESSAGES, INFO
from database.sessions_admin import admin_upcoming_sessions
from services.admin import format_sessions
from filters.admin import IsAdmin

router = Router()


@router.message(Command(commands='admin'), IsAdmin())
async def admin_start(message: Message):
    username = message.from_user.username
    await message.answer(INFO['/admin'].format(username), parse_mode='HTML')


@router.message(Command(commands='admin_upcoming'), IsAdmin())
async def admin_upcoming(message: Message):
    booked_sessions = admin_upcoming_sessions()
    response_message = format_sessions(booked_sessions)
    await message.answer(response_message, parse_mode='HTML')
