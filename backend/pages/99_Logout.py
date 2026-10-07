import streamlit as st
from src.auth import logout_user

logout_user()
st.info("You have been signed out.")
st.switch_page("pages/0_Login.py")
