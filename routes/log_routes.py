import re
from datetime import datetime
from fastapi import APIRouter, Response
from middleware.auth import require_auth

router = APIRouter()


@router.get("/")
def get_current_day_logs(token: str = require_auth()):
    """
    Get all logs for the current day.
    Returns an array of structured log entries with timestamp, level, and message.
    Handles multi-line log messages.
    """
    today = datetime.now().strftime("%d-%m-%Y")
    log_file = f"logs/{today}.log"

    try:
        with open(log_file, "r") as f:
            logs = f.read()

        # Parse logs using regex to split by timestamp pattern
        # Pattern: YYYY-MM-DD HH:MM:SS,mmm [LEVEL]: message
        log_pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})\s+\[([A-Z]+)\]:\s*(.*?)(?=\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}|$)"

        matches = re.finditer(log_pattern, logs, re.DOTALL)
        parsed_logs = []

        for match in matches:
            timestamp, level, message = match.groups()
            # Clean up message: strip trailing whitespace and newlines
            message = message.rstrip()
            parsed_logs.append({"timestamp": timestamp, "level": level, "message": message})

        return parsed_logs
    except FileNotFoundError:
        return Response(content=f"No logs found for {today}", status_code=404)
