import json
import os
from typing import List
from fastapi import APIRouter, Body, Depends, Response
from fastapi.params import Param

from database import get_db
from db_models.action import Action, ActionSchema
from db_models.setting import Setting, SettingKey
from helpers.models.text_prediction.gguf.gguf_text_prediction_model import GGUFTextPredictionModel
from helpers.models.text_prediction.text_prediction_model import TextPredictionModel
from middleware.auth import require_auth
from helpers.text_to_action.text_to_action import TextToAction
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/")
def convert_text_to_action(token: str = require_auth(), body: dict = Body(...), db: Session = Depends(get_db)):
    """
    Endpoint to convert text to action using TextToAction helper.
    """

    default_model: str = os.getenv("DEFAULT_TEXT_TO_ACTION_MODEL", "")

    text: str = body.get("text", "")
    model_name: str = body.get("model", default_model)

    if not text:
        return Response(content="text is required in the request body", status_code=422)

    # Get system prompt from settings
    system_prompt: str = Setting.get_setting(db, SettingKey.SYSTEM_PROMPT)

    actions: List[Action] = db.query(Action).all()
    actions_as_array: list = [ActionSchema.model_validate(a).model_dump() for a in actions]

    # Convert actions to an array
    system_prompt = system_prompt.replace("{actions}", json.dumps(actions_as_array))

    try:
        model: TextPredictionModel | None = GGUFTextPredictionModel(
            model_name=model_name,
            system_prompt=system_prompt,
        )
    except FileNotFoundError as e:
        return Response(content=str(e), status_code=422)

    text_to_action: TextToAction | None = TextToAction(model)

    # Get prediction timeout setting
    prediction_timeout_str: str = Setting.get_setting(db, SettingKey.PREDICTION_TIMEOUT)
    try:
        prediction_timeout: float = float(prediction_timeout_str)
    except ValueError:
        prediction_timeout = 5.0

    result: dict = text_to_action.convert_text_to_action(text, timeout=prediction_timeout)

    # Free up memory
    model = None
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
        return {"available_models": models}
    except Exception as e:
        return Response(content=str(e), status_code=500)
