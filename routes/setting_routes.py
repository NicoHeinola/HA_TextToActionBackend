from typing import List
from fastapi import APIRouter, Body, Depends, Response

from database import get_db
from db_models.setting import Setting
from middleware.auth import require_auth
from sqlalchemy.orm import Session

from seeders.setting_seeder import SettingSeeder

router = APIRouter()


@router.get("/")
def get_settings(token: str = require_auth(), db: Session = Depends(get_db)):
    """
    Endpoint to get application settings.
    """

    settings: List[Setting] = db.query(Setting).all()

    return settings


@router.post("/seed")
def seed_settings(token: str = require_auth(), db: Session = Depends(get_db), body: dict = Body(...)):
    replace: bool = body.get("replace", False)
    keys_to_seed: List[str] = body.get("keys_to_seed", [])

    SettingSeeder(db).seed(replace=replace, keys_to_seed=keys_to_seed)

    return Response(status_code=200)


@router.put("/{setting_id}")
def update_setting(setting_id: int, token: str = require_auth(), db: Session = Depends(get_db), body: dict = Body(...)):
    """
    Endpoint to update a specific setting by ID.
    """

    setting = db.query(Setting).filter(Setting.id == setting_id).first()
    if not setting:
        return Response(status_code=404, content="setting_not_found")

    blacklist_fields = ["id", "key", "type"]
    for field in body:
        if field in blacklist_fields:
            continue

        if hasattr(setting, field):
            setattr(setting, field, body[field])

    db.commit()

    return {
        "message": "setting_updated",
        "setting": setting,
    }
