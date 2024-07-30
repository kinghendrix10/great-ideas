# great-ideas/main.py
import streamlit as st
from pages import home, loading, analysis
from utils.report_generator import generate_report
import time

st.set_page_config(page_title="Great Ideas", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS to set black background and white text
st.markdown("""
    <style>
    .stApp {
        background-color: black;
        color: white;
    }
    .stTextInput > div > div > input {
        background-color: white;
        color: black;
    }
    .stButton > button {
        background-color: black;
        color: white;
        border: 1px solid white;
    }
    footer {
        visibility: hidden;
    }
    #MainMenu {
        visibility: hidden;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    if 'page' not in st.session_state:
        st.session_state.page = 'home'
    
    if 'user_input' not in st.session_state:
        st.session_state.user_input = ''
    
    if 'report_data' not in st.session_state:
        st.session_state.report_data = None

    if st.session_state.page == 'home':
        home.show()
    elif st.session_state.page == 'loading':
        loading.show()
        # Simulate processing time
        time.sleep(3)
        st.session_state.report_data = generate_report(st.session_state.user_input)
        st.session_state.page = 'analysis'
        st.experimental_rerun()
    elif st.session_state.page == 'analysis':
        analysis.show(st.session_state.report_data)

    # Footer
    st.markdown(
        '<div style="position: fixed; bottom: 0; left: 0; right: 0; background-color: black; padding: 10px;">'
        '<span style="float: left;">FAQ &nbsp;&nbsp; Terms &nbsp;&nbsp; AI Policy &nbsp;&nbsp; Privacy</span>'
        '</div>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
