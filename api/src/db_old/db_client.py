from sqlalchemy import create_engine
from src.db.migrations import run_migrations
from src.config import Config

import os

def init_db():
    engine = create_engine(Config.DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

    x = os.path.join(os.path.dirname(__file__), "api", "src", "db", "migrations")
    print(x)

    migrations_folder = os.path.join(os.path.dirname(__file__), "api", "src", "db", "migrations")
    run_migrations(engine, migrations_folder)
    return engine
