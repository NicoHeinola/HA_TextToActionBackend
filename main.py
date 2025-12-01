import logging
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from routes.index import router as index_router
from routes.text_to_action_routes import router as text_to_action_router
from routes.setting_routes import router as setting_router
from routes.action_routes import router as action_router
from routes.cache_routes import router as cache_router
from events.fast_api_events import lifespan

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(index_router)
app.include_router(text_to_action_router, prefix="/text-to-action")
app.include_router(setting_router, prefix="/settings")
app.include_router(action_router, prefix="/actions")
app.include_router(cache_router, prefix="/cache")


if __name__ == "__main__":
    load_dotenv()

    HOST: str = os.getenv("HOST", "")
    PORT: int = int(os.getenv("PORT", ""))
    HOT_RELOADING: bool = os.getenv("HOT_RELOADING", "False").lower() in ("true", "1", "t")

    if HOT_RELOADING:
        uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
    else:
        uvicorn.run(app=app, host=HOST, port=PORT)
