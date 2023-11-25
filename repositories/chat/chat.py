from contextlib import AbstractAsyncContextManager
from typing import Callable

from sqlalchemy import update
from sqlalchemy.exc import IntegrityError

from db.models.chat import Chat
from services.chat.interface import AbstractChatRepository


class ChatRepository(AbstractChatRepository):

    def __init__(self, session: Callable[..., AbstractAsyncContextManager]) -> None:
        self._session = session

    async def get(self, chat_id: int) -> Chat:
        """
        Получение чата по id

        :param chat_id: id чата

        :return: персонаж
        """
        async with self._session() as session:
            chat = session.get(Chat, chat_id)
            return chat

    async def create(self, chat_id: int) -> None:
        """
        Создание чата

        :param chat_id: id чата
        """
        async with self._session() as session:
            chat = Chat(chat_id=chat_id)
            session.add(chat)
            try:
                await session.commit()
            except IntegrityError:
                await session.rollback()

    async def get_start_message(self, chat_id: int) -> dict[str, str] | None:
        """
        Получение стартового сообщения

        :param chat_id: id чата

        :return: стартовое сообщение
        """
        async with self._session() as session:
            chat = await session.get(Chat, chat_id)
            if chat is None:
                return None
            return {"message": chat.start_message, "image": chat.start_image}

    async def update_start_message(self, chat_id: int, message: str, image: str) -> None:
        """
        Обновление стартового сообщения

        :param chat_id: id чата
        :param message: сообщение
        :param image: изображение
        """
        async with self._session() as session:
            sql = (
                update(Chat)
                .where(Chat.chat_id == chat_id)
                .values(start_message=message, start_image=image)
            )
            await session.execute(sql)
            await session.commit()
