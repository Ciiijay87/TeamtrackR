import streamlit as st
from _auth import sign_in, sign_up, sign_out, current_profile, is_staff, supa

# ============================
# STARTSEITE / LOGIN / SIGNUP
# ============================

st.set_page_config(page_title="TeamtrackR", page_icon="🏈", layout="wide")

# Sprachauswahl (optional)
lang = st.sidebar.selectbox("🌐 Sprache / Language", ["DE", "EN"])

# Session Setup
if "session" not in st.session_state:
    st.session_state["session"] = None

# Login oder Signup Tabs
tab1, tab2 = st.tabs(["Login", "Sign up"])

# ---------- LOGIN ----------
with tab1:
    st.subheader("Login")

    email = st.text_input("E-Mail")
    password = st.text_input("Passwort", type="password")

    if st.button("Login", type="primary"):
        try:
            res = sign_in(email, password)
            if res:
                st.success("✅ Erfolgreich eingeloggt.")
                st.session_state["session"] = res
                st.rerun()  # Hier statt experimental_rerun
            else:
                st.error("❌ Login fehlgeschlagen. Bitte überprüfe deine Daten.")
        except Exception as e:
            st.error(f"Fehler: {str(e)}")

# ---------- SIGNUP ----------
with tab2:
    st.subheader("Sign up")

    display_name = st.text_input("Anzeigename / Display name")
    email_su = st.text_input("E-Mail", key="signup_email")
    password_su = st.text_input("Passwort", type="password", key="signup_pw")

    if st.button("Registrieren", type="secondary"):
        try:
            res = sign_up(email_su, password_su, display_name)
            if res:
                st.success("✅ Registriert. Warte auf Freischaltung durch HC/TM.")
                st.session_state["session"] = None
                st.rerun()
            else:
                st.error("❌ Anmeldung fehlgeschlagen. Bitte erneut versuchen.")
        except Exception as e:
            st.error(f"Signup fehlgeschlagen: {str(e)}")

# ---------- STATUS ----------
st.divider()
st.caption("TeamtrackR © 2025 – Internal Team Management Prototype")

