from sqlalchemy import Column, Integer, String
from db_models.base import Base
from sqlalchemy.orm import Session


class SettingKey:
    SYSTEM_PROMPT = "system_prompt"
    PREDICTION_TIMEOUT = "prediction_timeout"
    DEFAULT_MODEL = "default_model"


class Setting(Base):
    __tablename__ = "settings"
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, nullable=False, index=True)
    value = Column(String, nullable=False)
    type = Column(String, nullable=False)  # 'int', 'string', 'float', 'boolean'

    @staticmethod
    def get_setting(db: Session, key: str) -> str:
        setting: Setting | None = db.query(Setting).filter(Setting.key == key).first()

        if setting is None:
            return ""

        return str(setting.value)
