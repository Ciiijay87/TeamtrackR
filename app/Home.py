import streamlit as st
from _auth import sign_in, sign_up, sign_out, current_profile, is_admin, is_staff

st.set_page_config(page_title="TeamtrackR", page_icon="🏈", layout="wide")

st.title("TeamtrackR")

prof = current_profile()
if prof:
    role = prof.get("role", "-")
    appr = "✅" if prof.get("approved") else "⏳"
    st.success(f"Willkommen, {prof.get('display_name','')} • Rolle: {role} • Freigabe: {appr}")

col1, col2 = st.columns(2)

with col1:
    st.header("Login")
    with st.form("login"):
        email = st.text_input("E-Mail", key="login_email")
        pwd = st.text_input("Passwort", type="password", key="login_pwd")
        ok = st.form_submit_button("Login")
        if ok:
            if sign_in(email, pwd):
                st.rerun()

with col2:
    st.header("Sign up")
    with st.form("signup"):
        disp = st.text_input("Anzeigename / Display name")
        semail = st.text_input("E-Mail")
        spwd = st.text_input("Passwort", type="password")
        submit = st.form_submit_button("Registrieren")
        if submit:
            if sign_up(semail, spwd, disp):
                st.info("Bitte bestätige deine E-Mail und warte auf Freischaltung (HC/TM).")

st.divider()
st.subheader("Schnellstart")
st.page_link("pages/1_Events.py", label="📅 Termine / Events")
st.page_link("pages/3_tasks.py", label="✅ Aufgaben / Tasks")
st.page_link("pages/2_Attendance.py", label="🟢 Anwesenheit")
st.page_link("pages/8_Gameweek.py", label="🗂️ Gameweek (Coming Soon)")
st.page_link("pages/11_Reports.py", label="📊 Reports (Coming Soon)")

if prof:
    if st.button("Logout"):
        sign_out()
        st.rerun()
