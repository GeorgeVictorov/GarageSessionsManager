import re
from aiogram import F, Router
from aiogram.types import Message, ContentType
from database.sqlite import Database, update_cached_users
from database.sessions_admin import clear_cache
from database.sessions_admin import admin_user_status
from config_data.config import load_config

router = Router()


@router.message(F.content_type == ContentType.TEXT)
async def process_phone_number(message: Message):
    db_manager = Database()
    user_id = message.from_user.id
    if admin_user_status(user_id) != 1:
        if not db_manager.check_user_registration(user_id):
            phone_number = message.text.strip()
            if not re.match(r'(?:\+7|8)?[- ]?\(?(9\d{2})\)?[- ]?(\d{3})[- ]?(\d{2})[- ]?(\d{2})', phone_number):
                await message.answer(
                    "<b>Invalid phone number format.</b>\n\n"
                    "Please provide your phone number in the following format:\n\n"
                    "For example: <b>+79261234455</b>\n\n"
                    "<i>By providing your phone number, you consent to the processing of your personal data.</i>\n\n"
                    "Please ensure that your phone number is correctly formatted to proceed.",
                    parse_mode='HTML')
            else:
                if phone_number.startswith('8'):
                    phone_number = '+7' + phone_number[1:]

                formatted_phone_number = re.sub(r'^(\+\d)(\d{3})(\d{3})(\d{2})(\d{2})$',
                                                r'\1 (\2) \3-\4-\5',
                                                phone_number)

                username = message.from_user.username
                db_manager.add_user(user_id, username, formatted_phone_number)
                update_cached_users()
                clear_cache()
                await message.answer(
                    f"<b>Thank you for providing your phone number:</b>"
                    f"\n\n<b>{formatted_phone_number}</b>\n\n"
                    f"<i>By providing your phone number, you consent to the processing of your personal data.</i>\n\n"
                    f"Press /start to begin.",
                    parse_mode='HTML')
                for admin_id in load_config().tg_bot.admin_ids:
                    admin_message = f'New user: <b>{username}</b> has registered.'
                    await message.bot.send_message(admin_id, admin_message, parse_mode='HTML')
    else:
        await message.answer('<b>You are banned.</b>', parse_mode='HTML')
