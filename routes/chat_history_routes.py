from typing import List
from fastapi import APIRouter, Body, Depends, Response

from database import get_db
from db_models.action import Action
from db_models.chat_history import ChatHistory
from middleware.auth import require_auth
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/")
def start_chat(token: str = require_auth(), db: Session = Depends(get_db)):
    """
    Starts a chat session for keeping history.
    """

    chat_history = ChatHistory()

    return chat_history
