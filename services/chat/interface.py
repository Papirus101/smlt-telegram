from abc import ABC
from db.models.chat import Chat


class AbstractChatRepository(ABC):

    async def get(self, chat_id: int) -> Chat:
        """
        Получение чата по id

        :param chat_id: id чата

        :return: персонаж
        """
        raise NotImplementedError

    async def create(self, chat_id: int) -> None:
        """
        Создание чата

        :param chat_id: id чата
        """
        raise NotImplementedError

    async def get_start_message(self, chat_id: int) -> dict[str, str] | None:
        """
        Получение стартового сообщения

        :param chat_id: id чата

        :return: стартовое сообщение
        """
        raise NotImplementedError

    async def update_start_message(self, chat_id: int, message: str, image: str) -> None:
        """
        Обновление стартового сообщения

        :param chat_id: id чата
        :param message: сообщение
        :param image: изображение
        """
        raise NotImplementedError
