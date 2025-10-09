import streamlit as st
from _auth import require_login

st.set_page_config(page_title="Gameweek", page_icon="🗂️", layout="wide")
require_login()

st.title("Gameweek Plan")
st.info("Coming soon – diese Seite wird gerade entwickelt. 👷‍♂️")
