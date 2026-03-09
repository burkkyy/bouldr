from sqlalchemy import create_engine
import os

# This creates/connects to 'database.sqlite' in the current working directory's api/src/db/db-vol folder
db_path = os.path.join(os.path.dirname(__file__), "src", "db", "db-vol", "database.sqlite")
DATABASE_URL = f"sqlite:///{db_path}"

engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})