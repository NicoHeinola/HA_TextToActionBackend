import os
from fastapi import APIRouter, Body, Response

from middleware.auth import require_auth
from helpers.text_to_action.text_to_action import TextToAction

router = APIRouter()


@router.post("/")
def convert_text_to_action(token: str = require_auth(), body: dict = Body(...)):
    """
    Endpoint to convert text to action using TextToAction helper.
    """

    text: str = body.get("text", "")

    if not text:
        return Response(content="text is required in the request body", status_code=422)

    text_to_action: TextToAction = TextToAction()
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
