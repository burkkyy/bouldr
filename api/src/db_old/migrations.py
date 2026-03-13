import os
from sqlalchemy import text

def run_migrations(engine, migrations_dir):
    """
    Reads .sql files from migrations_dir and applies them to the database
    if they haven't been applied yet.
    """
    print(f"Checking for migrations in: {migrations_dir}")
    
    if not os.path.exists(migrations_dir):
        os.makedirs(migrations_dir)
        print("Migrations directory did not exist. Created it.")
        return

    with engine.begin() as conn:
        # 1. Create a table to track migration history if it doesn't exist
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS schema_migrations (
                version TEXT PRIMARY KEY,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))

        result = conn.execute(text("SELECT version FROM schema_migrations"))
        applied_migrations = {row[0] for row in result}

        # Sorting is critical so 001_... runs before 002_...
        files = sorted(f for f in os.listdir(migrations_dir) if f.endswith('.sql'))
        
        pending_migrations = [f for f in files if f not in applied_migrations]

        if not pending_migrations:
            print("Database is up to date. No new migrations to apply.")
            return

        for file in pending_migrations:
            print(f"Applying migration: {file} ...")
            filepath = os.path.join(migrations_dir, file)
            
            with open(filepath, 'r') as f:
                sql_script = f.read()

            # SQLite handles multiple SQL statements best via its native executescript method.
            # We access the raw DBAPI connection from SQLAlchemy to use it.
            raw_conn = conn.connection.dbapi_connection
            cursor = raw_conn.cursor()
            
            try:
                cursor.executescript(sql_script)
                # Record that this migration was successfully applied
                conn.execute(
                    text("INSERT INTO schema_migrations (version) VALUES (:version)"), 
                    {"version": file}
                )
                print(f"Success: {file}")
            except Exception as e:
                print(f"Failed to apply {file}. Error: {e}")
                raise 
