import streamlit as st
from _auth import sign_in, sign_up, sign_out, current_profile, is_admin
import streamlit.components.v1 as components

st.set_page_config(page_title="TeamtrackR", page_icon="🏈", layout="wide")

# -------------------------------------------------------------------
# 1) JS-Brücke: Supabase leitet mit URL-Fragment (#access_token=...)
#    Streamlit sieht das nicht. Wir wandeln es einmalig in ?confirmed=1 um.
#    -> Keine Sicherheitswirkung, nur UI-Hinweis.
# -------------------------------------------------------------------
components.html("""
<script>
(function () {
  try {
    const u = new URL(window.location.href);
    // Nur handeln, wenn ein Hash mit Supabase-Token da ist
    if (window.location.hash && window.location.hash.includes('access_token')) {
      // Schon markiert? dann nichts tun
      if (!u.searchParams.get('confirmed')) {
        u.searchParams.set('confirmed','1');       // Flag für Streamlit
        history.replaceState(null, '', u.toString());  // URL ohne Reload umschreiben
        // Streamlit rerun anstoßen
        window.dispatchEvent(new Event('popstate'));
      }
    }
  } catch(e) {}
})();
</script>
""", height=0)

# -----------------------------
# Query-Params lesen (jetzt inkl. confirmed=1)
# -----------------------------
def qp(name: str):
  try:
    q = st.experimental_get_query_params()
  except Exception:
    q = st.query_params
  v = q.get(name)
  if isinstance(v, list):
    return v[0] if v else ""
  return v or ""

# Flash via Session
flash = st.session_state.pop("flash", None)

# Erfolgsmeldungen
if qp("confirmed") == "1":
    st.success("✅ E-Mail bestätigt. Jetzt noch Freischaltung durch Headcoach/Team Manager abwarten.")
if flash == "signup_ok":
    st.info("✅ Registrierung erfolgreich. Prüfe deine E-Mails und bestätige deine Adresse.")
elif flash == "login_ok":
    st.success("✅ Erfolgreich eingeloggt.")

# Sprache (optional)
if "lang" not in st.session_state:
    st.session_state["lang"] = "DE"
st.session_state["lang"] = st.sidebar.selectbox("🌐 Sprache / Language", ["DE", "EN"], index=0)

# Aktuelles Profil
prof = current_profile()

# =========================================================
# Nicht eingeloggt → Login / Sign up
# =========================================================
if not prof:
    st.title("🏈 TeamtrackR")

    col1, col2 = st.columns(2)

    # Login
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

    # Sign up
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
                st.session_state["flash"] = "signup_ok"
                st.rerun()
            except Exception as e:
                st.error(f"Signup fehlgeschlagen: {e}")

    st.caption("Hinweis: Nach der Registrierung E-Mail bestätigen. Danach schaltet dich der Headcoach/Team Manager frei.")
    st.stop()

# =========================================================
# Eingeloggt: Status
# =========================================================
st.info(f"Willkommen, {prof.get('display_name','')}  •  Rolle: {prof.get('role','?')}  •  Freigabe: {'✅' if prof.get('approved') else '⏳'}")

if not prof.get("approved", False):
    st.warning("Dein Zugang ist erstellt und die E-Mail ist bestätigt – **aber du bist noch nicht freigeschaltet**. Bitte HC oder TM informieren.")
    if st.button("Logout"):
        sign_out()
    st.stop()

# =========================================================
# Freigeschaltet → Kacheln
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
    ("🛠️ Admin", "12_Admin.py" if is_admin(prof) else None),
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

st.caption("TeamtrackR © 2025 – Internal Team Management Prototype")
