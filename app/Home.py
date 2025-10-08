# app/Home.py
import streamlit as st
from _auth import sign_in, sign_up, sign_out, get_session, current_profile
from _i18n import t

st.set_page_config(page_title="TeamtrackR", layout="wide")

lang = st.session_state.get("lang", "DE")
left, right = st.columns([1,1])

st.markdown(f"### {t('home.title', lang)}")

sess = get_session()
prof = current_profile()

with left:
    st.subheader("Login")
    email = st.text_input("E-Mail", key="login_email")
    pwd = st.text_input("Passwort", type="password", key="login_pwd")
    if st.button("Login"):
        ok = sign_in(email, pwd)
        if ok:
            st.success("Eingeloggt.")
            st.rerun()
        else:
            st.error("Login fehlgeschlagen (E-Mail bestätigt?).")

with right:
    st.subheader("Sign up")
    dn = st.text_input("Anzeigename / Display name", key="su_dn")
    em = st.text_input("E-Mail", key="su_email")
    pw = st.text_input("Passwort", type="password", key="su_pwd")
    if st.button("Registrieren"):
        if dn and em and pw:
            if sign_up(em, pw, dn):
                st.success("Registriert. Bitte E-Mail bestätigen; HC/TM schalten dich danach frei.")
            else:
                st.error("Signup fehlgeschlagen.")
        else:
            st.warning("Bitte alle Felder ausfüllen.")

st.divider()

# Quick Links (robust, ohne Icon-Parameter)
c1, c2, c3 = st.columns(3)
with c1:
    st.page_link("pages/1_Events.py", label=t("home.subtitle.events", lang))
with c2:
    st.page_link("pages/2_Attendance.py", label=t("home.subtitle.attendance", lang))
with c3:
    st.page_link("pages/3_tasks.py", label=t("home.subtitle.tasks", lang))

if prof:
    st.info(f"Willkommen, {prof.get('display_name', '')} · Rolle: {prof.get('role')} · Freigabe: {'✅' if prof.get('approved') else '⏳'}")
    if st.button("Logout"):
        sign_out()
