from sqlalchemy import Column, Integer, String, JSON
from db_models.base import Base


class Action(Base):
    __tablename__ = "actions"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True, index=True)
    description = Column(String, nullable=True)
    meta = Column(JSON, nullable=True, default={})
