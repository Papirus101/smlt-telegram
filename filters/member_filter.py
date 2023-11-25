from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery

import os


class SelfMember(Filter):
    async def __call__(self, query_or_message: Message | CallbackQuery) -> bool:
        new_members_ids = [member.id for member in query_or_message.new_chat_members]
        return os.getenv("BOT_ID") in new_members_ids
