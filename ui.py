import streamlit as st

def apply_style():
    st.markdown("""
    <style>
    .card {
        padding:20px;
        border-radius:15px;
        background:#1f2937;
        color:white;
        margin:10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

def card(title, content):
    st.markdown(f"<div class='card'><h3>{title}</h3><p>{content}</p></div>", unsafe_allow_html=True)

def header(text):
    st.markdown(f"<h1 style='color:#00ffae'>{text}</h1>", unsafe_allow_html=True)