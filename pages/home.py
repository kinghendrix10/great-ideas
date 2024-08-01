# great-ideas/pages/home.py
# File: data_analysis_app/pages/home.py
import streamlit as st

def process_input():
    if st.session_state.user_input:
        st.session_state.page = 'loading'
        st.session_state.start_analysis = True

def show():
    st.markdown("<h1 style='text-align: center; color: white;'>Great Ideas</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #ADD8E6;'>Let's make that idea great!</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,3,1])
    with col2:
        st.text_input("Business Idea", label_visibility="collapsed", placeholder="Description of your business idea and target audience", key="user_input", on_change=process_input)
        st.button("→", on_click=process_input)

    if 'user_input' in st.session_state and st.session_state.user_input == "":
        st.error("Please enter your business idea before proceeding.")