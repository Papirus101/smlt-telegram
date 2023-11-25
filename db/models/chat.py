from sqlalchemy import Column, BIGINT, VARCHAR

from db.base import Base


class Chat(Base):
    __tablename__ = "chat"

    chat_id = Column(BIGINT, unique=True, primary_key=True, autoincrement=False)
    start_message = Column(VARCHAR(255), nullable=True)
    start_image = Column(VARCHAR(255), nullable=True)
