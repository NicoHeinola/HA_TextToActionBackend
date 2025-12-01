from datetime import datetime
from fastapi import APIRouter, Response
from middleware.auth import require_auth

router = APIRouter()


@router.get("/")
def get_current_day_logs(token: str = require_auth()):
    """
    Get all logs for the current day.
    """
    today = datetime.now().strftime("%d-%m-%Y")
    log_file = f"logs/{today}.log"

    try:
        with open(log_file, "r") as f:
            logs = f.read()
        return {"date": today, "logs": logs}
    except FileNotFoundError:
        return Response(content=f"No logs found for {today}", status_code=404)
