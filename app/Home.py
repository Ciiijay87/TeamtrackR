import streamlit as st
from _i18n import t, lang_selector
from _auth import sign_in, sign_up, sign_out, current_profile

st.set_page_config(page_title="TeamtrackR", page_icon="🏈", layout="wide")
lang_selector()

st.markdown("<style>.stApp {max-width: 1200px; margin: 0 auto;}</style>", unsafe_allow_html=True)

def logged_in() -> bool:
    return current_profile() is not None

def banner_after_redirect():
    params = st.query_params
    if "access_token" in params or (params.get("type") == "signup"):
        st.success(t("E-Mail bestätigt. Du kannst dich jetzt einloggen.",
                     "Email confirmed. You can now log in."))
        st.query_params.clear()
banner_after_redirect()

st.title("TeamtrackR")

prof = current_profile()
if prof:
    role = prof.get("role", "player")
    approved = prof.get("approved", False)

    st.success(
        t(
            f"Willkommen, {prof.get('display_name','')} • Rolle: {role} • Freigabe: {'✅' if approved else '❌'}",
            f"Welcome, {prof.get('display_name','')} • Role: {role} • Approved: {'✅' if approved else '❌'}",
        )
    )
    if not approved:
        st.warning(t("Dein Zugang ist noch nicht freigeschaltet. Bitte warte auf Freigabe durch HC/TM.",
                     "Your account is not approved yet. Please wait for HC/TM approval."))

    c1, c2, c3 = st.columns(3)
    with c1:
        st.page_link("pages/1_Events.py", label=t("📅 Termine / Events", "📅 Events"), icon="📅")
        st.page_link("pages/2_Attendance.py", label=t("✅ Anwesenheit / Attendance", "✅ Attendance"), icon="✅")
    with c2:
        st.page_link("pages/3_tasks.py", label=t("📝 Tasks", "📝 Tasks"), icon="📝")
        st.page_link("pages/6_Roster.py", label=t("👥 Roster", "👥 Roster"), icon="👥")
    with c3:
        st.page_link("pages/7_Depth_Chart.py", label=t("📋 Depth Chart", "📋 Depth Chart"), icon="📋")
        st.page_link("pages/12_Admin.py", label=t("🛠️ Admin", "🛠️ Admin"), icon="🛠️")

    st.divider()
    if st.button(t("Abmelden", "Sign out")):
        try:
            sign_out()
        finally:
            st.rerun()

else:
    left, right = st.columns(2)

    with left:
        st.subheader(t("Login", "Login"))
        with st.form("login_form", clear_on_submit=False):
            email = st.text_input("E-Mail", key="login_email")
            pwd = st.text_input(t("Passwort", "Password"), type="password", key="login_pwd")
            submit = st.form_submit_button("Login")
            if submit:
                try:
                    ok = sign_in(email, pwd)
                    if ok:
                        st.success(t("Erfolgreich eingeloggt.", "Logged in successfully."))
                        st.rerun()
                    else:
                        st.error(t("Login fehlgeschlagen.", "Login failed."))
                except Exception as e:
                    st.error(t("Login fehlgeschlagen.", "Login failed.") + f" ({e})")

    with right:
        st.subheader("Sign up")
        with st.form("signup_form", clear_on_submit=False):
            display = st.text_input(t("Anzeigename / Display name", "Display name"), key="su_display")
            email2  = st.text_input("E-Mail", key="su_email")
            pwd2    = st.text_input(t("Passwort", "Password"), type="password", key="su_pwd")
            submit2 = st.form_submit_button(t("Registrieren", "Register"))
            if submit2:
                try:
                    ok2 = sign_up(email2, pwd2, display)
                    if ok2:
                        st.success(
                            t("Registriert. Bitte bestätige deine E-Mail. Danach schaltet dich der Headcoach/Team Manager frei.",
                              "Registered. Please confirm your email. Then HC/Team Manager will approve you.")
                        )
                    else:
                        st.error(t("Registrierung fehlgeschlagen.", "Registration failed."))
                except Exception as e:
                    st.error(t("Registrierung fehlgeschlagen.", "Registration failed.") + f" ({e})")

    st.caption(
        t("Hinweis: Nach der Registrierung E-Mail bestätigen. Danach schaltet dich der Headcoach/Team Manager frei.",
          "Note: After registering, confirm your email. Then HC/Team Manager will approve you.")
    )
