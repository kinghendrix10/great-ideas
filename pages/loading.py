# great-ideas/pages/loading.py
import streamlit as st

def show():
    st.markdown("<h1 style='text-align: center; color: white;'>Analyzing your idea...</h1>", unsafe_allow_html=True)
    
    # Display a spinner
    with st.spinner(''):
        st.markdown(
            """
            <style>
            .stSpinner > div > div {
                border-top-color: white !important;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        st.empty()  # This is where the spinner will appear
