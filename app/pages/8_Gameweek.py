import streamlit as st
from _auth import require_login, is_staff, supa
prof = require_login()
st.title("Gameweek Plan")

plans = supa().table("gameweek").select("*").execute().data
for g in plans:
    st.write(f"{g['day']}: {g['content']} ({g['responsible']})")

if is_staff(prof):
    with st.form("newplan"):
        day = st.text_input("Tag")
        content = st.text_area("Inhalt")
        resp = st.text_input("Verantwortlich")
        ok = st.form_submit_button("Speichern")
    if ok:
        supa().table("gameweek").insert({"day":day,"content":content,"responsible":resp,"created_by":prof["id"]}).execute()
        st.success("Plan gespeichert."); st.experimental_rerun()
