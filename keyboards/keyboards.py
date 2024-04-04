from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


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
