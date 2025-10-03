import streamlit as st
from _auth import require_login, is_staff, supa
prof = require_login()
st.title("Depth Chart")

depth = supa().table("depth_chart").select("*").execute().data
for d in depth:
    st.write(f"{d['position']}: {d['starter']} / {d.get('backup1','')} / {d.get('backup2','')}")

if is_staff(prof):
    with st.form("newdepth"):
        pos = st.selectbox("Position", ["QB","RB","WR","TE","OL","DL","LB","DB","K","P"])
        starter = st.text_input("Starter")
        b1 = st.text_input("Backup1")
        b2 = st.text_input("Backup2")
        ok = st.form_submit_button("Speichern")
    if ok:
        supa().table("depth_chart").upsert({"position":pos,"starter":starter,"backup1":b1,"backup2":b2}).execute()
        st.success("Gespeichert."); st.experimental_rerun()
