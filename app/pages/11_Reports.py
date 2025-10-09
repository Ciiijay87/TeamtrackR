import streamlit as st
from _auth import require_login

st.set_page_config(page_title="Reports", page_icon="📊", layout="wide")
require_login()

st.title("Reports")
st.info("Coming soon – diese Seite wird gerade entwickelt. 👷‍♀️")
