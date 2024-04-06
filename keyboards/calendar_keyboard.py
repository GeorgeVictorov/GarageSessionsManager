import calendar
from datetime import datetime
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from filters.callback_factory import ChooseDateCallback


def get_current_or_specified_date(year=None, month=None) -> datetime:
    if year is None or month is None:
        current_date = datetime.now()
    else:
        current_date = datetime(year, month, 1)
    return current_date


def generate_calendar(year=None, month=None) -> InlineKeyboardMarkup:
    current_date = get_current_or_specified_date(year, month)
    days_in_month = calendar.monthcalendar(current_date.year, current_date.month)
    calendar_markup = InlineKeyboardMarkup(inline_keyboard=[])

    calendar_markup.inline_keyboard.append([
        InlineKeyboardButton(text=current_date.strftime("%B %Y"), callback_data="ignore")
    ])

    for week in days_in_month:
        row = []
        for day in week:
            if day == 0:
                row.append(InlineKeyboardButton(text=" ", callback_data="ignore"))
            else:
                row.append(InlineKeyboardButton(text=str(day), callback_data=ChooseDateCallback(
                    year=f'{current_date.year}',
                    month=f'{current_date.month:02d}',
                    day=f'{day:02d}').pack()
                                                ))
        calendar_markup.inline_keyboard.append(row)

    calendar_markup.inline_keyboard.append([
        InlineKeyboardButton(text="<", callback_data=f"prev-{current_date.year}-{current_date.month:02d}"),
        InlineKeyboardButton(text=">", callback_data=f"next-{current_date.year}-{current_date.month:02d}")
    ])

    calendar_markup.inline_keyboard.append([
        InlineKeyboardButton(text="✔️ Confirm", callback_data='confirm_calendar')
    ])

    calendar_markup.inline_keyboard.append([
        InlineKeyboardButton(text='➖ Close️', callback_data='close_user'),
    ])

    return calendar_markup
