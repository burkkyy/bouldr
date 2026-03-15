import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env.development")


class Config:
    NODE_ENV = os.getenv("NODE_ENV", "development")
    TZ = os.getenv("TZ", "UTC")
    API_PORT = os.getenv("API_PORT", "5000")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("SQLALCHEMY_DATABASE_URI environment variable is not set")
