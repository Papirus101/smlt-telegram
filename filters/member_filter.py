from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery

import os


class SelfMember(Filter):
    async def __call__(self, query_or_message: Message | CallbackQuery) -> bool:
        new_members_ids = [member.id for member in query_or_message.new_chat_members]
        return int(os.getenv("BOT_ID")) in new_members_ids


class AdminFilter(Filter):
    async def __call__(self, query_or_message: Message | CallbackQuery) -> bool:
        admins = await query_or_message.chat.get_administrators()
        admin_ids = [admin.user.id for admin in admins]
        return query_or_message.from_user.id in admin_ids
