from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from lexicon.lexicon import MESSAGES, INFO
from database.sessions_admin import admin_upcoming_sessions
from config_data.config import load_config

router = Router()


@router.message(Command(commands='admin'))
async def admin_start(message: Message):
    username = message.from_user.username
    await message.answer(INFO['/admin'].format(username), parse_mode='HTML')


@router.message(Command(commands='admin_upcoming'))
async def admin_upcoming(message: Message):
    config = load_config()
    if message.from_user.id in config.tg_bot.admin_ids:
        booked_sessions = admin_upcoming_sessions()

        if booked_sessions:
            sessions_info = "\n".join([
                f"Session ID: <b>{user_session['id']}</b>\n"
                f"Start Time: <b>{user_session['session_start'].split()[0]} | "
                f"{user_session['session_start'].split()[1][:5]}</b>\n"
                f"Duration: <b>{user_session['duration']}</b> hours\n"
                f"Session Type: <b>{user_session['type_desc']}</b>\n"
                for user_session in booked_sessions
            ])
            response_message = MESSAGES['/a_upcoming'].format(sessions_info)
        else:
            response_message = "<b>There are no upcoming sessions.</b>"

        await message.answer(response_message, parse_mode='HTML')
    else:
        await message.answer(MESSAGES['/admin_upcoming'])
