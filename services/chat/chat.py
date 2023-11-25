from handler_services.chat.interface import AbstractChatService
from services.chat.interface import AbstractChatRepository


class ChatService(AbstractChatService):

    def __init__(self, chat_repository: AbstractChatRepository) -> None:
        self._chat_repository = chat_repository

    async def get_start_message(self, chat_id: int) -> dict[str, str]:
        """
        Получение стартового сообщения
        :param chat_id:
        :return:
        """
        return await self._chat_repository.get_start_message(chat_id)

    async def create(self, chat_id: int) -> None:
        """
        Создание чата
        :param chat_id:
        :return:
        """
        await self._chat_repository.create(chat_id)

    async def get(self, chat_id: int) -> dict[str, str]:
        """
        Получение чата по id
        :param chat_id:
        :return:
        """
        return await self._chat_repository.get(chat_id)

    async def update_start_message(self, chat_id: int, message: str, image: str) -> None:
        """
        Обновление стартового сообщения
        :param chat_id:
        :param message:
        :param image:
        :return:
        """
        await self._chat_repository.update_start_message(chat_id, message, image)