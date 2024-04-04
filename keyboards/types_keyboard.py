from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config_data.sessions_config import TYPES


def generate_types_duration(hours=3, disable_less=False) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    types_row = [InlineKeyboardButton(text=t, callback_data=t) for t in TYPES]
    keyboard.inline_keyboard.append(types_row)

    hours_row = [
        InlineKeyboardButton(text='-', callback_data=f'less-{hours}' if not disable_less else 'ignore'),
        InlineKeyboardButton(text=str(hours), callback_data='ignore'),
        InlineKeyboardButton(text='+', callback_data=f'more-{hours}')
    ]
    keyboard.inline_keyboard.append(hours_row)

    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text='✔️Confirm', callback_data='confirm_types'),
    ])
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text='🔙 Back to calendar', callback_data='return_types'),
    ])

    return keyboard
