from dependency_injector import containers, providers

from constants import DB_LINK
from db.session import Database

from dotenv import load_dotenv

from handler_services.chat.chat import ChatHandler
from repositories.chat.chat import ChatRepository
from services.chat.chat import ChatService


class BotContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    load_dotenv(".env")
    config.db.db_user.from_env("DB_USER", as_=str, required=True)
    config.db.db_pass.from_env("DB_PASS", as_=str, required=True)
    config.db.db_host.from_env("DB_HOST", as_=str, required=True)
    config.db.db_port.from_env("DB_PORT", as_=int, required=True)
    config.db.db_name.from_env("DB_NAME", as_=str, required=True)
    config.bot.token.from_env("BOT_TOKEN", as_=str, required=True)

    db_url = DB_LINK.format(
        db_user=config.db.db_user(),
        db_pass=config.db.db_pass(),
        db_host=config.db.db_host(),
        db_port=config.db.db_port(),
        db_name=config.db.db_name(),
    )

    db = providers.Singleton(Database, db_url=db_url)

    chat_repository = providers.Factory(ChatRepository, session=db.provided.session)
    chat_service = providers.Factory(ChatService, chat_repository=chat_repository)
    chat_handler = providers.Factory(ChatHandler, chat_service=chat_service)
