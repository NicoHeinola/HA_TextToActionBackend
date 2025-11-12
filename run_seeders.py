import logging
import traceback
from dotenv import load_dotenv
from database import SessionLocal
from sqlalchemy.orm import Session

from seeders.setting_seeder import SettingSeeder

load_dotenv(override=False)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")


logger = logging.getLogger(__name__)


def run_seeders(db: Session):
    SettingSeeder(db).seed(replace=False)


if __name__ == "__main__":
    db = SessionLocal()
    try:
        logger.info("Starting database seeding...")
        run_seeders(db)
        logger.info("Database seeding completed successfully.")
    except Exception as e:
        logger.error(f"Seeding failed: {traceback.format_exc()}")
    finally:
        db.close()
