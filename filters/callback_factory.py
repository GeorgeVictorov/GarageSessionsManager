from aiogram.filters.callback_data import CallbackData


class ChooseDateCallback(CallbackData, prefix='choose', sep='-'):
    year: str
    month: str
    day: str


class ChooseHourCallback(CallbackData, prefix='hour', sep='-'):
    hour: str


class CancelSessionCallback(CallbackData, prefix='cancel_session', sep='-'):
    id: str
