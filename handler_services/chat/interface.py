from abc import ABC


class AbstractChatService(ABC):

    async def get_start_message(self, chat_id: int) -> dict[str, str]:
        """
        Получение стартового сообщения

        :param chat_id: id чата

        :return: стартовое сообщение
        """
        raise NotImplementedError

    async def create(self, chat_id: int) -> None:
        """
        Создание чата

        :param chat_id: id чата
        """
        raise NotImplementedError

    async def get(self, chat_id: int) -> dict[str, str]:
        """
        Получение чата по id

        :param chat_id: id чата

        :return:
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
