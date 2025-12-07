from sqlalchemy import Column, Integer
from db_models.base import Base
from pydantic import BaseModel
from typing import Optional


class ChatHistory(Base):
    __tablename__ = "chat_history"
    id = Column(Integer, primary_key=True)


class ChatHistorySchema(BaseModel):
    id: int

    class Config:
        from_attributes = True
