import os
from dotenv import load_dotenv

load_dotenv("../.env.development")

class Config:
    NODE_ENV = os.getenv("NODE_ENV", "development")
    TZ = os.getenv("TZ", "UTC")
    DATABASE_URL = os.getenv("DATABASE_URL")

    print(f"Config: NODE_ENV={NODE_ENV}, TZ={TZ}, DATABASE_URL={DATABASE_URL}")

    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable is not set")
