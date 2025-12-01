import logging
from typing import Dict, List

from helpers.models.text_prediction.gguf.gguf_text_prediction_model import GGUFTextPredictionModel
from helpers.models.text_prediction.text_prediction_model import TextPredictionModel


logger = logging.getLogger(__name__)

cached_models: Dict[str, TextPredictionModel] = {}


def auto_cached_models(models: List[Dict[str, str]]) -> None:
    for model_info in models:
        model_name = model_info.get("name")
        model_type = model_info.get("type")

        if not model_name or not model_type:
            continue

        model: TextPredictionModel | None = None
        if model_type == "gguf":
            model = GGUFTextPredictionModel(model_name)

        if not model:
            continue

        logger.info(f"Auto-caching model: {model_name} of type {model_type}")
        cache_model(model_name, model)


def cache_model(model_name: str, model: TextPredictionModel) -> None:
    global cached_models

    cached_models[model_name] = model


def get_cached_model(model_name: str) -> TextPredictionModel | None:
    global cached_models

    return cached_models.get(model_name)


def get_all_cached_models() -> Dict[str, TextPredictionModel]:
    global cached_models

    return cached_models.copy()


def remove_cached_model(model_name: str) -> bool:
    global cached_models

    if model_name in cached_models:
        del cached_models[model_name]
        return True

    return False


def clear_all_cached_models() -> int:
    global cached_models

    count = len(cached_models)
    cached_models.clear()

    return count


def get_cached_models_list() -> List[str]:
    global cached_models

    return list(cached_models.keys())
