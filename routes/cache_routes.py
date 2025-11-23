from fastapi import APIRouter, Body, Response
from helpers.cache.model_cache import (
    cache_model,
    get_cached_models_list,
    remove_cached_model,
    clear_all_cached_models,
)
from helpers.models.text_prediction.gguf.gguf_text_prediction_model import GGUFTextPredictionModel
from helpers.models.text_prediction.text_prediction_model import TextPredictionModel
from middleware.auth import require_auth

router = APIRouter()


@router.get("/")
def get_cache(token: str = require_auth()):
    """
    Get all cached models.
    """
    cached_models = get_cached_models_list()
    return cached_models


@router.post("/")
def cache_new_model(token: str = require_auth(), body: dict = Body(...)):
    """
    Cache a new model.
    """

    model_name: str = body.get("model_name", "")

    if not model_name:
        return Response(content="model_name is required", status_code=422)

    model: TextPredictionModel = GGUFTextPredictionModel(model_name=model_name)
    cache_model(model_name, model)

    return Response(status_code=200)


@router.delete("/{model_name}")
def remove_model_from_cache(model_name: str, token: str = require_auth()):
    """
    Remove a specific model from cache.
    """
    if not model_name:
        return Response(content="model_name is required", status_code=422)

    success = remove_cached_model(model_name)

    if success:
        return Response(status_code=200)
    else:
        return Response(content=f"Model '{model_name}' not found in cache", status_code=404)


@router.delete("/")
def clear_cache(token: str = require_auth()):
    """
    Remove all models from cache.
    """
    count = clear_all_cached_models()
    return Response(status_code=200)
