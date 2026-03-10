from sqlalchemy import create_engine
from migrations import run_migrations
import os

# This creates/connects to 'database.sqlite' in the current working directory's api/src/db/db-vol folder
db_path = os.path.join(os.path.dirname(__file__), "api", "src", "db", "db-vol", "database.sqlite")
DATABASE_URL = f"sqlite:///{db_path}"

engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

migrations_folder = os.path.join(os.path.dirname(__file__), "api", "src", "db", "migrations")
run_migrations(engine, migrations_folder)