from . import connect_db
from sqliter import DatabaseError
from typing import Dict

class TransactionBackend:
    
    def __init__(self):
        self.db = connect_db()
    
    def add_transaction(self, info: Dict):
        try:
            self.db.query("""
            INSERT INTO Transactions (student_id, amount, taken_by) 
            VALUES (?, ?, ?)
            """, (info["student_id"], info["amount"], info["taken_by"]))
            
            return "🟢 Transaction Added Successfully."
        except DatabaseError as e:
            return f"😳 Error: {e}"
    
    def get_transaction_info(self, id: int):
        try:
            transaction_info = self.db.query("""
                SELECT * FROM Transactions WHERE id=?;
            """, (id, ), operation="fetchone")

            return transaction_info
        except DatabaseError as e:
            return f"😳 Error: {e}" 

    def get_transaction_list(self):
        try:
            transaction_list = self.db.query("""
                SELECT s.id, s.serial_number, s.student_name, amount, sf.name
                  FROM Transactions AS t
                  JOIN Students AS s ON t.student_id=s.id
                  JOIN Staff AS sf ON t.taken_by=sf.id;
            """, operation="fetchall")
            return transaction_list
        except DatabaseError as e:
            return f"😳 Error: {e}" 
        
    def update_transaction(self, info: Dict):
        try:
            self.db.query("""
                UPDATE Transactions
                SET student_id=?, amount=?, taken_by=? 
                WHERE id = ?
            """, (info["student_id"], info["amount"], info["taken_by"], info["id"]))

            return "🟢 Transaction Updated Successfully."
        except DatabaseError as e:
            return f"😳 Error: {e}"