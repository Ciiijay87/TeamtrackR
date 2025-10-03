import streamlit as st
from _auth import require_login, is_staff, supa
prof = require_login()
st.title("Roster")

players = supa().table("roster").select("*").order("number").execute().data
for p in players:
    st.write(f"#{p.get('number','?')} {p.get('firstname','')} {p.get('lastname','')} — {p.get('position1','')} — {p.get('status','fit')}")

if is_staff(prof):
    with st.form("newplayer"):
        fn = st.text_input("Vorname")
        ln = st.text_input("Nachname")
        nr = st.text_input("Nummer")
        pos = st.selectbox("Position", ["QB","RB","WR","TE","OL","DL","LB","DB","K","P"])
        submit = st.form_submit_button("Spieler speichern")
    if submit:
        supa().table("roster").insert({"firstname":fn,"lastname":ln,"number":nr,"position1":pos,"status":"fit"}).execute()
        st.success("Spieler gespeichert."); st.experimental_rerun()
