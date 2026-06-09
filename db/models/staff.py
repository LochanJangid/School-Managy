from . import connect_db
from sqliter import DatabaseError
from typing import Dict

class StaffBackend:
    
    def __init__(self):
        self.db = connect_db()
    
    def add_staff(self, info: Dict):
        try:
            self.db.query("""
            INSERT INTO Staff (name, designation) VALUES (?, ?)
            """, (info["name"], info["designation"]))
            
            return f"🟢 Staff Added Successfully."
        except DatabaseError as e:
            return f"😳 Error: {e}"
    
    def get_staff_info(self, id: int):
        try:
            staff_info = self.db.query("""
                SELECT * FROM Staff WHERE id=?;
            """, (id, ), operation="fetchone")

            return staff_info
        except DatabaseError as e:
            return "😳 Error: {e}"

    def get_staff_list(self):
         
        try:
            staff_list = self.db.query("""
                SELECT name, designation FROM Staff;
            """, operation="fetchall")
            return staff_list
        except DatabaseError as e:
            return "😳 Error: {e}"
        
    def update_staff(self, info: Dict):
        try:
            self.db.query("""
                UPDATE Staff
                SET name=?, designation=? 
                WHERE id = ?
            """, (info["name"], info["designation"], info["id"]), operation="fetchall")

            return f"🟢 Staff Updated Successfully."
        except DatabaseError as e:
            return "😳 Error: {e}"
            