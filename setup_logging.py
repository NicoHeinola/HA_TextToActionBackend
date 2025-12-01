import logging
import os
from logging.handlers import TimedRotatingFileHandler


def setup_logging():
    """Configure logging with date-based rotation."""
    # Ensure logs directory exists
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger()

    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()

    logger.setLevel(logging.INFO)

    # Configure logging with date-based rotation
    log_formatter = logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s")
    log_handler = TimedRotatingFileHandler("logs/app.log", when="midnight", interval=1, backupCount=30, utc=False)
    log_handler.setFormatter(log_formatter)

    # Use a proper namer that gets the current date at rotation time
    def namer(filename):
        import datetime as dt

        # Extract the base name and add the current date
        base = filename.replace(".log", "")
        return f"{base}.{dt.datetime.now().strftime('%Y-%m-%d')}.log"

    log_handler.namer = namer
    logger.addHandler(log_handler)
