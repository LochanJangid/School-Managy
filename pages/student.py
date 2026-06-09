import streamlit as st
import pandas as pd
from st_keyup import st_keyup
import datetime

# Assuming you have this backend setup
from db.models.student import StudentBackend

class StudentLogic:
    def __init__(self):
        self.sb = StudentBackend()
        pass

    def add_student(self, info):
        return self.sb.add_student(info)
        # return "Student added successfully to database."
    
    def get_student_list(self):
        return self.sb.get_student_list()
        # return [] # Returning empty list for demonstration

class StudentUI:
    def __init__(self):
        st.title("Student Management 🎓")
        st.divider()

    def render_student_list(self, student_list):
        # Handle empty database gracefully
        if not student_list:
            df = pd.DataFrame()
        else:
            df = pd.DataFrame(student_list)
        
        df.columns = [
                "serial_number", "student_name", "mother_name", 
                "class", "medium", "rte", "dob", "gender"
            ]

        col1, col2 = st.columns([5, 1])
        with col1:
            st.subheader("Student Directory")
        with col2:
            # Change the page state instead of opening a dialog
            if st.button("➕ Add Student"):
                st.session_state.current_page = "add"
                st.rerun()
                
        search_query = st_keyup("Search Students", debounce=300)

        if search_query and not df.empty:
            mask = df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)
            filtered_df = df[mask]
        else:
            filtered_df = df
            
        st.dataframe(filtered_df, hide_index=True)

    def render_add_student_form(self):
        st.subheader("Register New Student")
        
        # A back button to return to the list without saving
        if st.button("⬅️ Back to List"):
            st.session_state.current_page = "list"
            st.rerun()

        with st.form("add_student_form"):
            # Using columns for a cleaner, full-page layout
            col1, col2 = st.columns(2)
            
            with col1:
                serial_number = st.number_input("Serial Number", min_value=1, step=1)
                student_name = st.text_input("Student Name *")
                father_name = st.text_input("Father's Name")
                address = st.text_input("Address")
                student_class = st.text_input("Class *", max_chars=5)
                dob = st.date_input("Date of Birth", min_value=datetime.date(2000, 1, 1))

            with col2:
                # Max chars help enforce the SQLite CHECK constraints on the UI level
                phone_number = st.text_input("Phone Number (10 Digits)", max_chars=10)
                mother_name = st.text_input("Mother's Name")
                medium = st.selectbox("Medium *", options=["E", "H"], format_func=lambda x: "English" if x == "E" else "Hindi")
                rte = st.selectbox("RTE *", options=["N", "Y"], format_func=lambda x: "No" if x == "N" else "Yes")
                gender = st.selectbox("Gender", options=["M", "F", "O"], format_func=lambda x: "Male" if x == "M" else ("Female" if x == "F" else "Other"))
            
            st.caption("* Required fields")
            submitted = st.form_submit_button("Save Student", type="primary") 

            if submitted:
                # Basic UI Validation before sending to DB
                if not student_name or not student_class:
                    st.error("Student Name and Class are required!")
                elif phone_number and (len(phone_number) != 10 or not phone_number.isdigit()):
                    st.error("Phone number must be exactly 10 digits.")
                else:
                    st.session_state.new_student = {
                        "serial_number": serial_number,
                        "student_name": student_name,
                        "father_name": father_name,
                        "mother_name": mother_name,
                        "class": student_class,
                        "medium": medium,
                        "rte": rte,
                        "dob": dob,
                        "gender": gender,
                        "address": address,
                        "phone_number": phone_number
                    }
                    # Send user back to the list page after successful submission
                    st.session_state.current_page = "list"
                    st.rerun()

    def show_msg(self, msg):
        st.success(msg) 

class StudentApp:
    def __init__(self):
        self.ui = StudentUI()
        self.logic = StudentLogic()
        
        # Initialize routing and data states
        if 'new_student' not in st.session_state:
            st.session_state.new_student = None
            
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "list"
    
    def run(self):
        # 1. Process Data First
        if st.session_state.new_student:
            result_msg = self.logic.add_student(st.session_state.new_student)
            self.ui.show_msg(result_msg)
            st.session_state.new_student = None

        # 2. Page Routing Logic
        if st.session_state.current_page == "list":
            students = self.logic.get_student_list()
            self.ui.render_student_list(students)    
            
        elif st.session_state.current_page == "add":
            self.ui.render_add_student_form()

# Run the App
app = StudentApp()
app.run()