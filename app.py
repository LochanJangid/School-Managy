import streamlit as st

def home():

    st.write("""
        # School Managy 🐼
    """)

    st.write("""
        ## A Simple & Clean but with vast Database Structure 💪.
    """)

pg = st.navigation([ "pages/student.py", "pages/staff.py", home])
pg.run()    