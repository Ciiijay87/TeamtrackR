import streamlit as st
from _auth import require_login, current_profile, is_staff, supa
from datetime import date

st.set_page_config(page_title="Anwesenheit")
st.header("✅ Anwesenheit")

sess = require_login()
prof = current_profile()
if not prof.get("approved"):
    st.warning("Dein Zugang ist noch nicht freigeschaltet. Warte auf Freigabe durch HC/TM.")
    st.stop()

# Helper: Events laden (nur in Zukunft & letzte 60 Tage)
def list_events(limit=200):
    return supa().table("events").select("*").order("start", desc=False).limit(limit).execute().data or []

# Helper: Anwesenheit lesen/schreiben
def get_attendance(event_id):
    rows = supa().table("attendance").select("*").eq("event_id", event_id).execute().data or []
    # in ein dict: user_id -> status
    d = {}
    for r in rows:
        d[r["user_id"]] = r["status"]
    return d

def save_attendance(event_id, user_id, status):
    supa().table("attendance").upsert({
        "event_id": event_id,
        "user_id": user_id,
        "status": status
    }).execute()

# Status-Farben
def color_for(status: str) -> str:
    if status == "present":
        return "✅"
    if status == "excused":
        return "🟦"  # blau
    if status == "late":
        return "🟧"  # orange
    return "🟥"      # absent/unknown

# Auswahl Event
events = list_events()
if not events:
    st.info("Noch keine Events.")
    st.stop()

event_titles = [f"{e['title']} – {e['start']}" for e in events]
sel = st.selectbox("Event wählen", options=list(range(len(events))),
                   format_func=lambda i: event_titles[i])
event = events[sel]
st.caption(f"Event-ID: {event.get('id')}")

# Roster (vereinfachte Ansicht: alle Profile)
roster = supa().table("profiles").select("id, display_name, role").execute().data or []

# Anwesenheit laden
att_map = get_attendance(event["id"])

st.subheader("Markieren")
for p in roster:
    uid = p["id"]
    cur = att_map.get(uid, "absent")
    col1, col2 = st.columns([3, 2])
    with col1:
        st.write(f"{color_for(cur)}  **{p['display_name']}**  ·  {p['role']}")
    with col2:
        new = st.selectbox(
            "Status",
            ["present", "excused", "late", "absent"],
            index=["present","excused","late","absent"].index(cur),
            key=f"att_{event['id']}_{uid}"
        )
        if new != cur:
            save_attendance(event["id"], uid, new)

st.success("Änderungen werden automatisch gespeichert.")

# Summen / Ampel
st.subheader("Übersicht")
counts = {"present":0, "excused":0, "late":0, "absent":0}
for v in get_attendance(event["id"]).values():
    counts[v] = counts.get(v,0)+1

st.write(
    f"✅ Anwesend: **{counts['present']}**  ·  "
    f"🟦 Entschuldigt: **{counts['excused']}**  ·  "
    f"🟧 Verspätet: **{counts['late']}**  ·  "
    f"🟥 Fehlend: **{counts['absent']}**"
)
