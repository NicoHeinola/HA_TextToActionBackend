import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from db_models.setting import Setting, SettingKey
from database import get_db
from helpers.cache.model_cache import auto_cache_models


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for FastAPI application."""
    # Startup
    try:
        db_generator = get_db()
        db = next(db_generator)
        try:
            models_to_cache: list = Setting.get_setting_value(db=db, key=SettingKey.AUTO_CACHE_MODELS)
        finally:
            next(db_generator, None)

        if isinstance(models_to_cache, list) and models_to_cache:
            auto_cache_models(models_to_cache)
    except Exception as e:
        logging.warning(f"Failed to auto-cache models on startup: {e}")

    yield
