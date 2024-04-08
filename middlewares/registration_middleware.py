from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from lexicon.lexicon import MESSAGES
from database.db import Database


class RegistrationMiddleware(BaseMiddleware):
    """Middleware to check if a user is registered in the database."""

    def __init__(self) -> None:
        pass

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        db_manager = Database()
        user_id = event.from_user.id
        is_registered = db_manager.check_user_registration(user_id)
        if not is_registered:
            await event.answer(MESSAGES['/registration'], parse_mode='HTML')
            return False
        return await handler(event, data)
