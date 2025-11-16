from typing import List
from fastapi import APIRouter, Body, Depends, Response

from database import get_db
from db_models.action import Action
from middleware.auth import require_auth
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/")
def get_actions(token: str = require_auth(), db: Session = Depends(get_db)):
    """
    Endpoint to get application actions.
    """

    actions: List[Action] = db.query(Action).all()

    return actions


@router.put("/{action_id}")
def update_action(action_id: int, token: str = require_auth(), db: Session = Depends(get_db), body: dict = Body(...)):
    """
    Endpoint to update a specific action by ID.
    """

    action = db.query(Action).filter(Action.id == action_id).first()
    if not action:
        return Response(status_code=404, content="action_not_found")

    meta = body.get("meta")
    if meta and type(meta) is not dict:
        return Response(status_code=422, content="meta_must_be_dict")

    blacklist_fields = ["id"]
    for field in body:
        if field in blacklist_fields:
            continue

        if hasattr(action, field):
            setattr(action, field, body[field])

    db.commit()
    db.refresh(action)

    return action


@router.post("/")
def create_action(token: str = require_auth(), db: Session = Depends(get_db), body: dict = Body(...)):
    """
    Endpoint to create a new action.
    """

    meta = body.get("meta")
    if meta and type(meta) is not dict:
        return Response(status_code=422, content="meta_must_be_dict")

    action = Action()
    blacklist_fields = ["id"]
    for field in body:
        if field in blacklist_fields:
            continue

        if hasattr(action, field):
            setattr(action, field, body[field])

    db.add(action)
    db.commit()
    db.refresh(action)

    return action


@router.delete("/{action_id}")
def delete_action(action_id: int, token: str = require_auth(), db: Session = Depends(get_db)):
    """
    Endpoint to delete a specific action by ID.
    """

    action = db.query(Action).filter(Action.id == action_id).first()
    if not action:
        return Response(status_code=404, content="action_not_found")

    db.delete(action)
    db.commit()

    return Response(status_code=204)


@router.delete("/")
def delete_all_actions(token: str = require_auth(), db: Session = Depends(get_db)):
    """
    Endpoint to delete all actions.
    """

    db.query(Action).delete()
    db.commit()

    return Response(status_code=204)
