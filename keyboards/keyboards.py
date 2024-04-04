from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.sessions_user import upcoming_sessions


def generate_confirm_session() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text='✔️Confirm session', callback_data='session'),
    ])
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text='🔙 Back to types', callback_data='return_session'),
    ])

    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text='✖️️ Cancel', callback_data='cancel_session'),
    ])

    return keyboard


def generate_sessions_keyboard(user_id):
    booked_sessions = upcoming_sessions(user_id)
    keyboard_markup = InlineKeyboardMarkup(inline_keyboard=[])
    if booked_sessions:
        for user_session in booked_sessions:
            session_info = (
                f"{user_session['session_start'].split()[0]} | {user_session['session_start'].split()[1][:5]} | "
                f"{user_session['duration']} hours | "
                f"{user_session['type_desc']}"
            )
            keyboard_markup.inline_keyboard.append([InlineKeyboardButton(text=session_info,
                                                                         callback_data=f"cancel_session-{user_session['id']}")])
    return keyboard_markup
