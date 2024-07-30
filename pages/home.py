# great-ideas/pages/home.py
import streamlit as st

def show():
    st.markdown("<h1 style='text-align: center; color: white;'>Great Ideas</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #ADD8E6;'>Let's make that idea great!</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,3,1])
    with col2:
        user_input = st.text_input("", placeholder="Description of your business idea and target audience", key="user_input")
        if st.button("→"):
            if user_input:
                st.session_state.user_input = user_input
                st.session_state.page = 'loading'
                st.experimental_rerun()
            else:
                st.error("Please enter your business idea before proceeding.")
