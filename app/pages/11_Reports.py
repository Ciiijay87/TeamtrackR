import streamlit as st
from _auth import require_login, is_staff, supa
prof = require_login()
st.title("Reports")

if not is_staff(prof):
    st.warning("Nur Staff/Coaches")
    st.stop()

tab1, tab2 = st.tabs(["Attendance","Verletzungen"])

with tab1:
    data = supa().table("attendance").select("*").execute().data
    st.write("Gesamte Attendance-Einträge:", len(data))

with tab2:
    inj = supa().table("injuries").select("*").execute().data
    st.write("Verletzungen:", len(inj))
