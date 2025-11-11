import traceback
from dotenv import load_dotenv
from database import SessionLocal
from sqlalchemy.orm import Session

load_dotenv(override=False)


def run_seeders(db: Session):
    pass


if __name__ == "__main__":
    db = SessionLocal()
    try:
        print("Running seeders...")
        run_seeders(db)
        print("Seeders finished.")
    except Exception as e:
        print(f"Seeding failed: {traceback.format_exc()}")
    finally:
        db.close()
