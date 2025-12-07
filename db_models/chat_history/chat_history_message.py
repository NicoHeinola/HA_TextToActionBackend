from sqlalchemy import Column, Integer, String, Text, ForeignKey
from db_models.base import Base
from pydantic import BaseModel
from typing import Optional


class ChatHistoryMessageType:
    USER = "user"
    AI = "AI"


class ChatHistoryMessage(Base):
    __tablename__ = "chat_history_message"
    id = Column(Integer, primary_key=True)
    chat_history_id = Column(Integer, ForeignKey("chat_history.id", ondelete="CASCADE"), nullable=False)
    message = Column(Text, nullable=True, index=True)
    type = Column(String, nullable=True)  # e.g., 'user' or 'AI'


class ChatHistoryMessageSchema(BaseModel):
    id: int
    chat_history_id: int
    message: Optional[str] = None
    type: Optional[str] = None

    class Config:
        from_attributes = True
