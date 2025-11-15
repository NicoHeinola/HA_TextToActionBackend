import json
import os
from typing import List
from fastapi import APIRouter, Body, Depends, Response

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

    text: str = body.get("text", "")

    if not text:
        return Response(content="text is required in the request body", status_code=422)

    system_prompt: str = Setting.get_setting(db, SettingKey.SYSTEM_PROMPT)

    actions: List[Action] = db.query(Action).all()
    actions_as_array: list = [ActionSchema.model_validate(a).model_dump() for a in actions]

    # Convert actions to an array
    system_prompt = system_prompt.replace("{actions}", json.dumps(actions_as_array))

    model: TextPredictionModel = GGUFTextPredictionModel(
        model_name="Phi-3-mini-4k-instruct-q4.gguf",
        system_prompt=system_prompt,
    )

    text_to_action: TextToAction = TextToAction(model)

    result: dict = text_to_action.convert_text_to_action(text)
    return result


@router.get("/models")
def list_models(token: str = require_auth(), body: dict = Body(...)):
    """
    Endpoint to list available text-to-action models.
    """
    model_type: str = body.get("model_type", "")

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
