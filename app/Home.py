import streamlit as st
from _auth import sign_in, sign_up, sign_out, current_profile, get_session, is_admin

st.set_page_config(page_title="TeamtrackR", layout="wide")

st.title("TeamtrackR")

# ---- Top Badge (falls eingeloggt) ----
sess = get_session()
prof = current_profile() if sess else None
if prof:
    badge = f"Willkommen, {prof.get('display_name')} • Rolle: {prof.get('role')} • Freigabe: {'✅' if prof.get('approved') else '⏳'}"
    st.info(badge)

# ---- Tabs: Login / Sign up ----
left, right = st.columns(2)

with left:
    st.subheader("Login")
    email = st.text_input("E-Mail", key="login_email")
    pwd = st.text_input("Passwort", type="password", key="login_pwd")
    if st.button("Login", use_container_width=False):
        ok = sign_in(email, pwd)
        if ok:
            st.success("Eingeloggt.")
            st.rerun()
        else:
            st.error("Login fehlgeschlagen.")

with right:
    st.subheader("Sign up")
    dn = st.text_input("Anzeigename / Display name", key="su_dn")
    email2 = st.text_input("E-Mail", key="su_email")
    pwd2 = st.text_input("Passwort", type="password", key="su_pwd")
    if st.button("Registrieren", use_container_width=False):
        if not dn or not email2 or not pwd2:
            st.error("Bitte alle Felder ausfüllen.")
        else:
            sign_up(email2, pwd2, dn)
            st.success("Registriert. Bestätige bitte deine E-Mail. Danach schaltet dich Headcoach/Team Manager frei.")

st.divider()

# ---- Links zu Seiten (ohne Emojis/Icons, robust für ältere Streamlit-Versionen) ----
st.write("Schnellzugriff:")
col1, col2, col3 = st.columns(3)
with col1:
    st.page_link("pages/1_Events.py", label="Kalender")
with col2:
    st.page_link("pages/2_Attendance.py", label="Anwesenheit")
with col3:
    st.page_link("pages/3_tasks.py", label="Tasks")

# ---- Logout, falls eingeloggt ----
if sess:
    if st.button("Logout"):
        sign_out()
