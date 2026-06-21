import streamlit as st
import pandas as pd
from st_keyup import st_keyup

from db.models.transaction import TransactionBackend
from db.models.staff import StaffBackend

class TransactionLogic:
    def __init__(self):
        self.tb = TransactionBackend()
        self.sb = StaffBackend()
        pass

    def add_transaction(self, info):
        return self.tb.add_transaction(info)
    
    def get_transaction_list(self):
        return self.tb.get_transaction_list()
    
    def get_staff_list(self):
        raw_staff = self.sb.get_staff_list()

        if not raw_staff:
            return []

        return [dict(row) for row in raw_staff]

class TransactionUI:
    def __init__(self):
        st.title("Transaction Management 💳")
        st.divider()

    def render_transaction_list(self, transaction_list):
        df = pd.DataFrame(transaction_list)
        
        df.columns = ["student_id", "Serial Number", "Student Name", "amount", "taken_by"]

        col1, col2 = st.columns([5, 1])
        with col1:
            st.subheader("Transaction Ledger")
        with col2:
            if st.button("➕ New Transaction"):
                st.session_state.current_page = "add"
                st.rerun()
                
        search_query = st_keyup("Search Transactions (by Student ID, Staff ID, etc.)", debounce=300)

        if search_query and not df.empty:
            mask = df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)
            filtered_df = df[mask]
        else:
            filtered_df = df
            
        st.dataframe(filtered_df)

    def render_add_transaction_form(self, staff_list):
        st.subheader("Record New Transaction")
        
        if st.button("⬅️ Back to Ledger"):
            st.session_state.current_page = "list"
            st.rerun()

        with st.form("add_transaction_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                student_id = st.number_input("Student ID (Foreign Key) *", min_value=1, step=1)

            with col2:
                amount = st.number_input("Amount *", min_value=0.0, step=10.0, format="%.2f")
                taken_by = st.selectbox(
                    "Taken By / Staff Member *",
                    options=staff_list,
                    format_func=lambda x: x["name"]
                )

            st.caption("* Required fields")
            submitted = st.form_submit_button("Save Transaction", type="primary") 

            if submitted:
                # Basic UI Validation
                if amount <= 0:
                    st.error("Amount must be greater than zero.")
                else:
                    st.session_state.new_transaction = {
                        "student_id": student_id,
                        "amount": amount,
                        "taken_by": taken_by["id"]
                    }
                    st.session_state.current_page = "list"
                    st.rerun()

    def show_msg(self, msg):
        st.success(msg) 

class TransactionApp:
    def __init__(self):
        self.ui = TransactionUI()
        self.logic = TransactionLogic()
        
        if 'new_transaction' not in st.session_state:
            st.session_state.new_transaction = None
            
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "list"
    
    def run(self):
        # 1. Process Data
        if st.session_state.new_transaction:
            result_msg = self.logic.add_transaction(st.session_state.new_transaction)
            self.ui.show_msg(result_msg)
            st.session_state.new_transaction = None

        # 2. Routing
        if st.session_state.current_page == "list":
            transactions = self.logic.get_transaction_list()
            self.ui.render_transaction_list(transactions)    
            
        elif st.session_state.current_page == "add":
            self.ui.render_add_transaction_form(self.logic.get_staff_list())

# Run the App
app = TransactionApp()
app.run()