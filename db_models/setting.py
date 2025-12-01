from typing import Any
from sqlalchemy import Column, Integer, String
from db_models.base import Base
from sqlalchemy.orm import Session
from pydantic import BaseModel, field_serializer
from helpers.setting.dynamic_type_converter import DynamicTypeConverter


class SettingKey:
    SYSTEM_PROMPT = "system_prompt"
    PREDICTION_TIMEOUT = "prediction_timeout"
    DEFAULT_MODEL = "default_model"


class SettingResponse(BaseModel):
    id: int
    key: str
    value: str
    type: str

    class Config:
        from_attributes = True

    @field_serializer("value")
    def serialize_value(self, value: str):
        """Convert value to proper type based on the type field."""
        return DynamicTypeConverter.to_type(value, self.type)


class Setting(Base):
    __tablename__ = "settings"
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, nullable=False, index=True)
    value = Column(String, nullable=False)
    type = Column(String, nullable=False)  # 'int', 'string', 'float', 'boolean'

    @staticmethod
    def get_setting_value(db: Session, key: str) -> Any:
        setting: Setting | None = db.query(Setting).filter(Setting.key == key).first()

        if setting is None:
            return ""

        return DynamicTypeConverter.to_type(setting.value, setting.type)
