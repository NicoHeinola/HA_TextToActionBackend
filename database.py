import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=False)

# Ensure the database_instance directory exists
SQLALCHEMY_DATABASE_URL: str = os.getenv("SQLALCHEMY_DATABASE_URL", "")
os.makedirs(os.path.dirname(SQLALCHEMY_DATABASE_URL), exist_ok=True)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    pool_size=100,
    max_overflow=100,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
