import streamlit as st
from _auth import require_login, is_staff, supa
from _data import get_roster, list_units, set_attendance

prof = require_login()
st.title("Anwesenheit / Attendance")

if not is_staff(prof):
    st.info("Nur Coaches/Staff können Anwesenheit erfassen.")
    st.stop()

events = supa().table("events").select("*").order("starts_at", desc=False).execute().data
event = st.selectbox("Training wählen", options=events, format_func=lambda e: f"{e['title']} – {e['starts_at']}") if events else None
if not event:
    st.info("Keine Events – erst einen Termin anlegen.")
    st.stop()

unit_filter = st.multiselect("Filter (Units)", list_units(), default=list_units())
roster = get_roster()
if unit_filter:
    roster = [r for r in roster if (r.get("position1") in unit_filter) or (r.get("position2") in unit_filter) or (r.get("position3") in unit_filter)]

st.write("Status: ✅ da (100), 🟠 spät (75), 🔵 entschuldigt (50), ❌ fehlt (0)")
for r in roster:
    pid = r["player_id"]
    name = r.get("contact") or pid
    col1, col2, col3, col4, col5 = st.columns([3,1,1,1,1])
    with col1:
        st.write(f"**#{r.get('number','?')} {r.get('position1','')}** – {name}")
    if col2.button("✅", key=f"p{pid}"):
        set_attendance(event["id"], pid, "present", prof["id"])
    if col3.button("🟠", key=f"l{pid}"):
        set_attendance(event["id"], pid, "late", prof["id"])
    if col4.button("🔵", key=f"e{pid}"):
        set_attendance(event["id"], pid, "excused", prof["id"])
    if col5.button("❌", key=f"a{pid}"):
        set_attendance(event["id"], pid, "absent", prof["id"])

st.success("Jeder Klick wird sofort gespeichert.")
