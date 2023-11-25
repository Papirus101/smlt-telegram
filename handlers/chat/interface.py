from abc import ABC

from aiogram.types import Message


class AbstractChatHandler(ABC):

    async def new_member(self, message: Message) -> None:
        """
        Обработка нового участника

        :param message: сообщение
        """
        raise NotImplementedError

    async def add_bot_to_chat(self, message: Message) -> None:
        """
        Добавление бота в чат

        :param message: сообщение
        """
        raise NotImplementedError

    async def update_start_message(self, message: Message) -> None:
        """
        Обновление стартового сообщения

        :param message: сообщение
        """
        raise NotImplementedError

    async def test_start_message(self, message: Message) -> None:
        """
        Тест стартового сообщения

        :param message: сообщение
        """
        raise NotImplementedError

    async def help(self, message: Message) -> None:
        """
        Помощь

        :param message: сообщение
        """
        raise NotImplementedError