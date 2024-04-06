from aiogram.filters.callback_data import CallbackData


class ChooseDateCallback(CallbackData, prefix='choose', sep='-'):
    year: str
    month: str
    day: str


class ChooseHourCallback(CallbackData, prefix='hour', sep='-'):
    hour: str


class CancelSessionCallback(CallbackData, prefix='cancel_session', sep='-'):
    id: str


class AdminCancelCallback(CallbackData, prefix='admin_cancel', sep='-'):
    id: str


class AdminPaymentCallback(CallbackData, prefix='admin_confirm', sep='-'):
    id: str
