from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message
from loguru import logger

from handler_services.chat.interface import AbstractChatService
from handlers.chat.interface import AbstractChatHandler


class ChatHandler(AbstractChatHandler):

    def __init__(self, chat_service: AbstractChatService):
        self.chat_service = chat_service

    async def new_member(self, message: Message) -> None:
        start_data = await self.chat_service.get_start_message(chat_id=message.chat.id)
        if not start_data:
            return
        for chat_member in message.new_chat_members:
            message_text = start_data["message"].format(
                first_name=chat_member.first_name,
                last_name=chat_member.last_name if chat_member.last_name else "",
            )
            if start_data["image"]:
                await message.answer_photo(photo=start_data["image"], caption=message_text)
            elif start_data["message"]:
                await message.answer(text=message_text)
            try:
                await message.delete()
            except TelegramBadRequest:
                pass

    async def add_bot_to_chat(self, message: Message) -> None:
        logger.info(f"Add bot to chat {message.chat.id}")
        await self.chat_service.create(chat_id=message.chat.id)

    async def update_start_message(self, message: Message) -> None:
        image = message.photo[-1].file_id if message.photo else None
        message_text = message.caption if message.caption else message.text
        message_text = message_text.replace("/update_start_message", "").strip()
        if not message_text:
            await message.answer("Вы не ввели сообщение", reply_to_message_id=message.message_id)
            await self.help(message=message)
            return
        await self.chat_service.update_start_message(
            chat_id=message.chat.id,
            message=message_text,
            image=image
        )
        message_text = ("Пример готово приветственного сообщения:\n\n"
                        + message_text.format(
                    first_name=message.from_user.first_name,
                    last_name=message.from_user.last_name if message.from_user.last_name else "")
                        )
        if image:
            await message.answer_photo(
                photo=image,
                caption=message_text
            )
        else:
            await message.answer(text=message_text)

    async def test_start_message(self, message: Message) -> None:
        start_data = await self.chat_service.get_start_message(chat_id=message.chat.id)
        if not start_data:
            await message.answer("Для этого чата не установлено приветственное сообщение", reply_to_message_id=message.message_id)
            return
        message_text = start_data["message"].format(
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name if message.from_user.last_name else "",
        )
        if start_data["image"]:
            await message.answer_photo(photo=start_data["image"], caption=message_text)
        elif start_data["message"]:
            await message.answer(text=message_text)

    async def help(self, message: Message) -> None:
        text = (
            "Бот для приветствий\n"
            "Команды\n"
            "/start_message - получить текущее приветствие\n"
            "/update_start_message - обновить приветствие\n"
            "/help - помощь\n\n"
            "Бот поддерживает следующие переменные:\n"
            "<code>{first_name}</code> - имя пользователя\n"
            "<code>{last_name}</code> - фамилия пользователя ( не у всех указана фамилия в ТГ, поэтому заменяется пустой строкой при отсутствии )\n\n"
            "Бот поддерживает HTML форматирование:\n"
            "<code>&lt;strong&gt;Жирный шрифт&lt;/strong&gt;</code>,\n"
            "<code>&lt;a href='http://www.example.com/'&gt;Ссылка в тексте&lt;/a&gt;</code>,\n"
            "<code>&lt;a href='tg://user?id=123456789'&gt;Ссылка на юзера в ТГ&lt;/a&gt;</code>,\n"
            "<code>&lt;code&gt;Моноширное форматирование&lt;/code&gt;</code>,\n"
            "Пример приветствия:\n"
            "/update_start_message Добро пожаловать, &lt;strong&gt;{first_name} {last_name}&lt;/strong&gt;\n\n"
            "Такое приветствие будет выглядеть так:\n"
            f"Добро пожаловать, <strong>{message.from_user.first_name} {message.from_user.last_name if message.from_user.last_name else ''}</strong>\n\n"
        )
        await message.answer(
            text=text,
        )
