from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ContentType
from dependency_injector.wiring import Provide, inject

from containers import BotContainer
from filters.member_filter import SelfMember, AdminFilter
from handlers.chat.interface import AbstractChatHandler

chat_router = Router()


@chat_router.message(F.content_type.in_({ContentType.NEW_CHAT_MEMBERS}), SelfMember())
@inject
async def add_bot_to_chat(
        message: Message,
        add_bot_to_chat_handler: AbstractChatHandler = Provide[BotContainer.chat_handler]
):
    await add_bot_to_chat_handler.add_bot_to_chat(message=message)


@chat_router.message(F.content_type.in_({ContentType.NEW_CHAT_MEMBERS, ContentType.LEFT_CHAT_MEMBER}))
@inject
async def new_member(
        message: Message,
        add_bot_to_chat_handler: AbstractChatHandler = Provide[BotContainer.chat_handler]
):
    await add_bot_to_chat_handler.new_member(message=message)


@chat_router.message(Command("update_start_message"), F.content_type(ContentType.PHOTO), AdminFilter())
@inject
async def update_start_message_with_photo(
        message: Message,
        add_bot_to_chat_handler: AbstractChatHandler = Provide[BotContainer.chat_handler]
):
    await add_bot_to_chat_handler.update_start_message(message=message)


@chat_router.message(Command("update_start_message"), AdminFilter())
@inject
async def update_start_message(
        message: Message,
        add_bot_to_chat_handler: AbstractChatHandler = Provide[BotContainer.chat_handler]
):
    await add_bot_to_chat_handler.update_start_message(message=message)


@chat_router.message(Command("start_message"))
@inject
async def get_start_message(
        message: Message,
        add_bot_to_chat_handler: AbstractChatHandler = Provide[BotContainer.chat_handler]
):
    await add_bot_to_chat_handler.test_start_message(message=message)


@chat_router.message(Command("help"))
@inject
async def help_handler(
        message: Message,
        add_bot_to_chat_handler: AbstractChatHandler = Provide[BotContainer.chat_handler]
):
    await add_bot_to_chat_handler.help(message=message)