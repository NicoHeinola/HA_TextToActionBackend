from sqlalchemy import Column, Integer, String, JSON
from db_models.base import Base
from pydantic import BaseModel
from typing import Optional, Dict, Any


class Action(Base):
    __tablename__ = "actions"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True, index=True)
    description = Column(String, nullable=True)
    meta = Column(JSON, nullable=True, default={})


class ActionSchema(BaseModel):
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    meta: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True
