import streamlit as st

def login():
    st.title("🔐 Enter patient details")

    name = st.text_input("Name")
    phone = st.text_input("Phone")

    if st.button("Login"):
        if name and phone:
            st.session_state.logged_in = True
            st.session_state.name = name
            st.rerun()
        