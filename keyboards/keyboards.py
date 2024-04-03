import datetime
import calendar
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
        InlineKeyboardButton(text='Confirm', callback_data='confirm_types'),
    ])
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text='Back to calendar', callback_data='return_types'),
    ])

    return keyboard


def get_current_or_specified_date(year=None, month=None) -> datetime:
    if year is None or month is None:
        current_date = datetime.datetime.now()
    else:
        current_date = datetime.datetime(year, month, 1)
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
                callback_data = f"choose-{current_date.year}-{current_date.month:02d}-{day:02d}"
                row.append(InlineKeyboardButton(text=str(day), callback_data=callback_data))
        calendar_markup.inline_keyboard.append(row)

    calendar_markup.inline_keyboard.append([
        InlineKeyboardButton(text="<", callback_data=f"prev-{current_date.year}-{current_date.month:02d}"),
        InlineKeyboardButton(text=">", callback_data=f"next-{current_date.year}-{current_date.month:02d}")
    ])

    calendar_markup.inline_keyboard.append([
        InlineKeyboardButton(text="Confirm", callback_data='confirm_calendar')
    ])

    return calendar_markup


def generate_hours_keyboard(selected_date: str) -> InlineKeyboardMarkup:
    hours_markup = InlineKeyboardMarkup(inline_keyboard=[])

    selected_date = datetime.datetime.strptime(selected_date, '%Y-%m-%d')
    start_time = datetime.datetime.combine(selected_date.date(), datetime.datetime.min.time())
    end_time = datetime.datetime.combine(selected_date.date(), datetime.datetime.max.time())

    # Define the interval for each hour (e.g., every hour)
    interval = datetime.timedelta(hours=1)

    current_time = start_time
    row = []
    while current_time <= end_time:
        # Add the hour as a button
        callback_data = f"choose-hour-{current_time.strftime('%H:%M')}"
        row.append(InlineKeyboardButton(text=current_time.strftime('%H:%M'), callback_data=callback_data))

        # Add a newline after every 3 buttons
        if len(row) == 4:
            hours_markup.inline_keyboard.append(row)
            row = []

        current_time += interval

    # Add the remaining buttons if any
    if row:
        hours_markup.inline_keyboard.append(row)

    # Add a button to go back to the calendar
    hours_markup.inline_keyboard.append([
        InlineKeyboardButton(text="Back to Calendar", callback_data="back_to_calendar")
    ])

    return hours_markup
