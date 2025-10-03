import streamlit as st
from _auth import sign_in, sign_up, sign_out, current_profile, is_staff

st.set_page_config(page_title="TeamtrackR", layout="wide")
if "lang" not in st.session_state:
    st.session_state["lang"] = "DE"

col_lang1, col_lang2 = st.columns([1,9])
with col_lang1:
    st.session_state["lang"] = st.selectbox("Sprache/Language", ["DE","EN"], label_visibility="collapsed")

st.title("TeamtrackR")

prof = current_profile()
if not prof:
    tab1, tab2 = st.tabs(["Login", "Sign up"])
    with tab1:
        with st.form("login"):
            email = st.text_input("E-Mail")
            pw = st.text_input("Passwort", type="password")
            ok = st.form_submit_button("Login")
        if ok:
            try:
                sign_in(email, pw)
                st.success("Eingeloggt.")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Login fehlgeschlagen: {e}")
    with tab2:
        with st.form("signup"):
            dn = st.text_input("Anzeigename / Display name")
            email2 = st.text_input("E-Mail")
            pw2 = st.text_input("Passwort", type="password")
            ok2 = st.form_submit_button("Registrieren")
        if ok2:
            try:
                sign_up(email2, pw2, dn)
                st.success("Registriert. Warte auf Freischaltung durch HC/TM.")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Signup fehlgeschlagen: {e}")
    st.stop()

st.info(f"Willkommen, {prof.get('display_name')} – Rolle: {prof.get('role')} – Freigabe: {'✅' if prof.get('approved') else '⏳'}")
if not prof.get("approved"):
    st.warning("Dein Zugang ist noch nicht freigeschaltet. Bitte HC/TM kontaktieren.")
    if st.button("Logout"):
        sign_out(); st.experimental_rerun()
    st.stop()

cols = st.columns(3)
tiles = [
    ("Termine / Events", "1_Events.py"),
    ("Anwesenheit / Attendance", "2_Attendance.py"),
    ("Aufgaben / Tasks", "3_Tasks.py"),
    ("Dateien", "4_Files.py"),
    ("Ankündigungen", "5_Announcements.py"),
    ("Roster", "6_Roster.py"),
    ("Depth Chart", "7_Depth_Chart.py"),
    ("Gameweek", "8_Gameweek.py"),
    ("Gameday", "9_Gameday.py"),
    ("Forum", "10_Forum.py"),
    ("Reports", "11_Reports.py"),
    ("Admin", "12_Admin.py" if is_staff(prof) else None),
]
i = 0
for label, page in tiles:
    if page is None: 
        continue
    with cols[i%3]:
        st.page_link("pages/"+page, label=label, icon="➡️")
    i += 1

if st.button("Logout"):
    sign_out(); st.experimental_rerun()
