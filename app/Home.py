import streamlit as st
from _auth import current_profile, require_login
from _i18n import t

st.set_page_config(page_title="TeamtrackR", page_icon="🏈", layout="wide")

# ---- Auth check ----
prof = require_login()
st.session_state["profile"] = prof

# Infozeile
role = prof.get("role", "player")
ok = "✅" if prof.get("approved") else "⏳"
st.success(f"Willkommen, {prof.get('display_name')}; Rolle: {role}; Freigabe: {ok}")

# Header
left, right = st.columns([1, 1])
with left:
    st.markdown("<h1 style='margin-bottom:0'>TeamtrackR</h1>", unsafe_allow_html=True)
    st.caption("Schnelle Übersicht")

# Kacheln (nutzen st.page_link – KEIN use_container_width!)
c1, c2, c3 = st.columns(3)

with c1:
    st.page_link("pages/1_Events.py", label="📅  Termine / Events")
with c2:
    st.page_link("pages/2_Attendance.py", label="✅  Anwesenheit")
with c3:
    st.page_link("pages/3_Tasks.py", label="🧾  Tasks / To-Dos")

# Mini-Widgets
st.markdown("---")
st.subheader("Schnellzugriff")

cc1, cc2 = st.columns(2)
with cc1:
    st.page_link("pages/6_Roster.py", label="👥 Roster öffnen")
    st.page_link("pages/4_Files.py", label="📁 Dateien")
with cc2:
    st.page_link("pages/11_Reports.py", label="📊 Reports")
    st.page_link("pages/12_Admin.py", label="🛠️ Admin")
