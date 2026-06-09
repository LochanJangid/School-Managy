from sqliter import Database

def connect_db():
    DB_PATH = "school_management.db"
    return Database(DB_PATH)