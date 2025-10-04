import streamlit as st
from _auth import sign_in, sign_up, sign_out, current_profile, is_staff

st.set_page_config(page_title="TeamtrackR", page_icon="🏈", layout="wide")

# -----------------------------
# Flash-Nachrichten (über Rerun)
# -----------------------------
flash = st.session_state.pop("flash", None)
if flash == "signup_ok":
    st.info("✅ Registrierung erfolgreich. Dein Zugang muss vom Headcoach/Team Manager freigeschaltet werden.")
elif flash == "login_ok":
    st.success("✅ Erfolgreich eingeloggt.")

# Sprache (optional)
if "lang" not in st.session_state:
    st.session_state["lang"] = "DE"
st.session_state["lang"] = st.sidebar.selectbox("🌐 Sprache / Language", ["DE", "EN"], index=0)

# Aktuelles Profil prüfen
prof = current_profile()

# =========================================================
# 1) Falls NICHT eingeloggt: Login/Sign-up anzeigen (Form)
# =========================================================
if not prof:
    st.title("🏈 TeamtrackR")

    col1, col2 = st.columns(2)

    # --------- LOGIN (Form verhindert Doppel-Submit) ---------
    with col1:
        st.subheader("Login")
        with st.form("login_form", clear_on_submit=False):
            email = st.text_input("E-Mail", key="login_email")
            pw = st.text_input("Passwort", type="password", key="login_pw")
            ok = st.form_submit_button("Login", use_container_width=True)
        if ok:
            try:
                sign_in(email, pw)
                st.session_state["flash"] = "login_ok"
                st.rerun()
            except Exception as e:
                st.error(f"Login fehlgeschlagen: {e}")

    # --------- SIGN-UP (Form + Flash + kein Doppel-Submit) ---------
    with col2:
        st.subheader("Sign up")
        with st.form("signup_form", clear_on_submit=False):
            display_name = st.text_input("Anzeigename / Display name", key="su_name")
            email_su = st.text_input("E-Mail", key="su_email")
            password_su = st.text_input("Passwort", type="password", key="su_pw")
            ok2 = st.form_submit_button("Registrieren", use_container_width=True)
        if ok2:
            try:
                _ = sign_up(email_su, password_su, display_name)
                # Hinweis: Bei Supabase ist nach sign_up meist KEINE Session aktiv.
                st.session_state["flash"] = "signup_ok"
                st.rerun()
            except Exception as e:
                st.error(f"Signup fehlgeschlagen: {e}")

    st.caption("Hinweis: Nach der Registrierung muss der Headcoach/Team Manager deinen Zugang freischalten.")
    st.stop()

# =========================================================
# 2) Eingeloggt, aber noch NICHT freigeschaltet
# =========================================================
st.info(f"Willkommen, {prof.get('display_name','')}  •  Rolle: {prof.get('role','?')}  •  Freigabe: {'✅' if prof.get('approved') else '⏳'}")

if not prof.get("approved", False):
    st.warning("Dein Zugang ist erstellt, aber **noch nicht freigeschaltet**. Bitte den Headcoach oder Team Manager informieren.")
    if st.button("Logout"):
        sign_out()
        st.rerun()
    st.stop()

# =========================================================
# 3) Eingeloggt & freigeschaltet → Kacheln
# =========================================================
st.title("🏈 TeamtrackR")

cols = st.columns(3)
tiles = [
    ("📅 Termine / Events", "1_Events.py"),
    ("✅ Anwesenheit / Attendance", "2_Attendance.py"),
    ("📝 Aufgaben / Tasks", "3_Tasks.py"),
    ("📂 Dateien", "4_Files.py"),
    ("📣 Ankündigungen", "5_Announcements.py"),
    ("👥 Roster", "6_Roster.py"),
    ("📊 Depth Chart", "7_Depth_Chart.py"),
    ("🗓️ Gameweek", "8_Gameweek.py"),
    ("🏟️ Gameday", "9_Gameday.py"),
    ("💬 Forum", "10_Forum.py"),
    ("📈 Reports", "11_Reports.py"),
    ("🛠️ Admin", "12_Admin.py" if is_staff(prof) else None),
]

i = 0
for label, page in tiles:
    if page is None:
        continue
    with cols[i % 3]:
        st.page_link("pages/" + page, label=label, icon="➡️", use_container_width=True)
    i += 1

st.divider()
if st.button("Logout"):
    sign_out()
    st.rerun()

st.caption("TeamtrackR © 2025 – Internal Team Management Prototype")
