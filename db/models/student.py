from . import connect_db
from sqliter import DatabaseError
from typing import Dict

class StudentBackend:
    
    def __init__(self):
        self.db = connect_db()
    
    def add_student(self, info: Dict):
        try:
            self.db.query("""
            INSERT INTO Students (serial_number, student_name, father_name, 
                          mother_name, address, phone_number, class, 
                          medium, rte, gender, dob) VALUES 
                          (?, ?, ?, 
                           ?, ?, ?, ?, 
                           ?, ?, ?, ?)
            """, (info["serial_number"], info["student_name"], info["father_name"],
                  info["mother_name"], info["address"], info["phone_number"], info["class"],
                  info["medium"], info["rte"], info["gender"], info["dob"]))
            
            return f"🟢 Staff Added Successfully."
        except DatabaseError as e:
            return f"😳 Error: {e}"
    
    def get_student_info(self, id: int):
        try:
            staff_info = self.db.query("""
                SELECT * FROM Students WHERE id=?;
            """, (id, ), operation="fetchone")

            return staff_info
        except DatabaseError as e:
            return "😳 Error: {e}"

    def get_student_list(self):
        try:
            staff_list = self.db.query("""
                SELECT serial_number, student_name, mother_name, 
                       class, medium, rte, dob, gender 
                  FROM Students;
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
            