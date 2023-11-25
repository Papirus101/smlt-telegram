import asyncio
import os

from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode
from aiogram.types import BotCommand, BotCommandScopeDefault
from loguru import logger

from containers import BotContainer

from handlers.chat import chat_handler


async def register_commands(bot: Bot):
    commands = [
        BotCommand(command="start_message", description="Текущее приветствие"),
        BotCommand(command="update_start_message", description="Обновить приветствие"),
        BotCommand(command="help", description="Помощь"),
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())


async def main() -> None:
    container = BotContainer()
    container.wire(
        modules=[
            chat_handler,
        ]
    )
    dp = Dispatcher()
    bot = Bot(container.config.bot.token(), parse_mode=ParseMode.HTML)
    await bot.delete_webhook(drop_pending_updates=True)
    await register_commands(bot)

    dp.include_router(chat_handler.chat_router)
    bot_info = await bot.me()
    logger.info(f"Запустили бота {bot_info.first_name} @{bot_info.username} {bot_info.id}")
    os.environ["BOT_ID"] = str(bot_info.id)

    bot.container = container

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
