from datetime import datetime, timedelta
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.sessions import get_unavailable_times


def generate_hours_keyboard(selected_date: str, selected_duration: int) -> InlineKeyboardMarkup:
    hours_markup = InlineKeyboardMarkup(inline_keyboard=[])

    selected_date = datetime.strptime(selected_date, '%Y-%m-%d')
    start_time = datetime.combine(selected_date.date(), datetime.min.time())
    end_time = datetime.combine(selected_date.date(), datetime.max.time())

    unavailable_times = get_unavailable_times(selected_date)
    unavailable_intervals = [
        (datetime.strptime(start, '%Y-%m-%d %H:%M:%S'), datetime.strptime(end, '%Y-%m-%d %H:%M:%S')) for start, end in
        unavailable_times]

    row = []

    for current_time in range(0, int((end_time - start_time).total_seconds() // 3600) + 1, 1):
        session_start = start_time + timedelta(hours=current_time)
        session_end = session_start + timedelta(hours=selected_duration)

        if any(start <= session_start < end or start < session_end <= end for start, end in unavailable_intervals):
            row.append(InlineKeyboardButton(text="Unavailable", callback_data="unavailable"))
        else:
            callback_data = f"hour-{session_start.strftime('%H:%M:%S')}"
            row.append(InlineKeyboardButton(text=session_start.strftime('%H:%M'), callback_data=callback_data))

        if len(row) == 4:
            hours_markup.inline_keyboard.append(row)
            row = []

    if row:
        hours_markup.inline_keyboard.append(row)

    hours_markup.inline_keyboard.extend([
        [InlineKeyboardButton(text="✔️ Confirm", callback_data="confirm_session")],
        [InlineKeyboardButton(text="🔙 Back to types", callback_data="back_to_types")]
    ])

    return hours_markup
