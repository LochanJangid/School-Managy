import os
from sqliter import Database, DatabaseError

def init_database():
    """Run all sql Schema Query from the CREATE TABLES files."""
    DB_DIR = os.path.dirname(os.path.abspath(__file__))
    SCHEMA_DIR = os.path.join(DB_DIR, "CREATE_TABLES")

    DB_PATH = "school_management.db"
    db = Database(DB_PATH)
    
    schema_files = ["FEES_STRUCTURE.sql", "STAFF.sql", "STUDENTS.sql", "TRANSACTIONS.sql"]

    for file in schema_files:
        file_path = os.path.join(SCHEMA_DIR, file)
        with open(file_path, "r") as f:
            sql_script = f.read()
        
            ## Execute DDL Commands
            try:
                db.query(sql_script)
            except DatabaseError as e:
                print(e)
            else:
                print("Done... 🐯")


if __name__ == "__main__":
    init_database()