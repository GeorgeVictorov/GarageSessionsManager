from aiogram.filters import BaseFilter
from aiogram.types import Message
from config_data.config import load_config


class IsAdmin(BaseFilter):
    def __init__(self) -> None:
        self.admin_ids = load_config().tg_bot.admin_ids

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admin_ids
