import streamlit as st
import pandas as pd
from st_keyup import st_keyup

from db.models.staff import StaffBackend

class StaffLogic:

    def __init__(self):
        self.sb = StaffBackend()

    def add_staff(self, info):
        return self.sb.add_staff(info)
    
    def get_staff_list(self):
        return self.sb.get_staff_list()

class StaffUI:
    def __init__(self):
        st.title("Staff Managy 🧑‍🏫")
        st.divider()

    def staff_list(self, staff_list):
        df = pd.DataFrame(staff_list)
        df.columns = ["id", "name", "designation"]

        col1, col2 = st.columns([5, 1])
        with col1:
            st.subheader("Staff List")
        with col2:
            if st.button("Add Staff"):
                self.render_add_staff_form()
        search_query = st_keyup("Search", debounce=300)

        if search_query:
            mask = df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)
            filtered_df = df[mask]
        else:
            filtered_df = df
        st.dataframe(filtered_df)
    
    @st.dialog("Add New Staff Member")
    def render_add_staff_form(self):
        with st.form("add_staff_form", clear_on_submit=True):
            name = st.text_input("Full Name")
            designation = st.text_input("Designation")
            submitted = st.form_submit_button("Submit") 

            if submitted:
                st.session_state.new_staff = {"name": name, "designation": designation}

                st.rerun()

    def show_msg(self, msg):
        st.success(msg) 

class Staff:
    def __init__(self):
        self.ui = StaffUI()
        self.logic = StaffLogic()
        
        if 'new_staff' not in st.session_state:
            st.session_state.new_staff = None
    
    def run(self):
        if st.session_state.new_staff:
            adding_staff = self.logic.add_staff(st.session_state.new_staff)
            self.ui.show_msg(adding_staff)
            st.session_state.new_staff = None
        staffs = self.logic.get_staff_list()
        self.ui.staff_list(staffs)    
        

app = Staff()
app.run()