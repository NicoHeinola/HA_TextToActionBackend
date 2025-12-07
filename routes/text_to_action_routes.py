import json
import os
from typing import List
from fastapi import APIRouter, Body, Depends, Response
from fastapi.params import Param

from database import get_db
from db_models.action import Action, ActionSchema
from db_models.setting import Setting, SettingKey
from helpers.cache.model_cache import get_cached_model
from helpers.models.text_prediction.gguf.gguf_text_prediction_model import GGUFTextPredictionModel
from helpers.models.text_prediction.text_prediction_model import TextPredictionModel
from middleware.auth import require_auth
from helpers.text_to_action.text_to_action import TextToAction
from sqlalchemy.orm import Session
from db_models.chat_history.chat_history_message import ChatHistoryMessage, ChatHistoryMessageSchema

router = APIRouter()


@router.post("/")
def convert_text_to_action(token: str = require_auth(), body: dict = Body(...), db: Session = Depends(get_db)):
    """
    Endpoint to convert text to action using TextToAction helper.
    """

    # --- Get prediction timeout setting
    default_model: str = Setting.get_setting_value(db, SettingKey.DEFAULT_MODEL)

    text: str = body.get("text", "")
    model_name: str = body.get("model", default_model)

    try:
        chat_history_id: int | None = int(body.get("chat_history_id", ""))
    except (ValueError, TypeError):
        chat_history_id = None

    if not model_name:
        return Response(content="Model is required in the request body. No default model set", status_code=422)

    if not text:
        return Response(content="text is required in the request body", status_code=422)

    # --- Get model from cache or load new one
    try:
        model = get_cached_model(model_name)

        if model is None:
            model: TextPredictionModel | None = GGUFTextPredictionModel(model_name=model_name)
    except FileNotFoundError as e:
        return Response(content=str(e), status_code=422)

    text_to_action: TextToAction | None = TextToAction(model)

    # --- Get prediction timeout setting
    prediction_timeout: float = Setting.get_setting_value(db, SettingKey.PREDICTION_TIMEOUT)

    # --- Get system prompt from settings
    system_prompt: str = Setting.get_setting_value(db, SettingKey.SYSTEM_PROMPT)

    # --- Get chat history
    messages: List[dict] = []
    if chat_history_id:
        chat_history_messages = (
            db.query(ChatHistoryMessage)
            .filter(ChatHistoryMessage.chat_history_id == chat_history_id)
            .order_by(ChatHistoryMessage.id.asc())
            .all()
        )

        messages = [ChatHistoryMessageSchema.model_validate(message).model_dump() for message in chat_history_messages]
        messages = [{"message": message.get("message"), "type": message.get("type")} for message in messages]

    actions: List[Action] = db.query(Action).all()
    actions_as_array: list = [ActionSchema.model_validate(action).model_dump() for action in actions]

    system_prompt = system_prompt.replace("{actions}", json.dumps(actions_as_array))
    system_prompt = system_prompt.replace("{chat_history}", json.dumps(messages))

    # --- Convert text to action
    result: dict = text_to_action.convert_text_to_action(system_prompt, text, timeout=prediction_timeout)

    # Free up memory (Don't free up the model itself since it can be used again)
    text_to_action = None

    return result


@router.get("/models")
def list_models(model_type: str, token: str = require_auth()):
    """
    Endpoint to list available text-to-action models.
    """
    # Sanitize
    model_type = model_type.strip().lower().replace(" ", "_").replace("-", "_").replace(".", "_").replace("/", "_")

    if not model_type:
        return Response(content="model_type is required in the request body", status_code=422)

    models_dir = os.path.join("models", "text_prediction", model_type)
    try:
        models = [
            name
            for name in os.listdir(models_dir)
            if os.path.isfile(os.path.join(models_dir, name))
            and not name.endswith(".md")
            or os.path.isdir(os.path.join(models_dir, name))
        ]

        return models
    except Exception as e:
        return Response(content=str(e), status_code=500)
