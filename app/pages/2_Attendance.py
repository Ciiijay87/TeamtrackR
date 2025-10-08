import streamlit as st
from _i18n import t, lang_selector
from _auth import supa, current_profile

st.set_page_config(page_title="Attendance", page_icon="✅", layout="wide")
lang_selector()

st.title(t("Anwesenheit", "Attendance"))

prof = current_profile()
if not prof:
    st.warning(t("Bitte einloggen.", "Please log in."))
    st.stop()

def is_staff_like(p: dict) -> bool:
    role = (p or {}).get("role", "player")
    return role in ["headcoach", "team_manager", "coach", "staff", "admin", "oc", "dc"]

# Event-Auswahl
event_id = None
events = []
try:
    res = supa().table("events").select("id,title,start").order("start", desc=False).limit(200).execute()
    events = res.data or []
except Exception as e:
    st.info(t("Tabelle 'events' nicht gefunden oder keine Leserechte.",
              "Table 'events' missing or no read access.") + f" ({e})")

labels = [f"{ev['title']} — {ev['start']}" for ev in events]
if events:
    idx = st.selectbox(t("Event wählen", "Select event"), range(len(events)), format_func=lambda i: labels[i])
    event_id = events[idx]["id"]
else:
    st.stop()

st.divider()

# Ampel-Status zusammenfassen
def status_emoji(s: str) -> str:
    s = (s or "").lower()
    return {"present": "🟢", "excused": "🟡", "absent": "🔴"}.get(s, "⚪️")

# Teilnehmerliste (read)
try:
    res = supa().table("attendance").select("*").eq("event_id", event_id).execute()
    rows = res.data or []
    if not rows:
        st.info(t("Noch keine Einträge.", "No entries yet."))
    else:
        for r in rows:
            name = r.get("display_name") or r.get("user_name") or r.get("user_id", "—")
            st.write(f"{status_emoji(r.get('status'))}  **{name}** — {r.get('status','')}")
except Exception as e:
    st.info(t("Tabelle 'attendance' nicht gefunden oder keine Leserechte.",
              "Table 'attendance' missing or no read access.") + f" ({e})")

# Status setzen (nur Staff)
if is_staff_like(prof):
    st.divider()
    st.subheader(t("Status setzen", "Set status"))
    with st.form("set_att"):
        uid = st.text_input(t("User-ID (oder Name, je nach Schema)", "User ID (or name, depending on schema)"))
        status = st.selectbox(t("Status", "Status"), ["present", "excused", "absent"])
        submit = st.form_submit_button(t("Speichern", "Save"))
        if submit:
            try:
                supa().table("attendance").upsert({
                    "event_id": event_id,
                    "user_id": uid,
                    "status": status,
                    "updated_by": prof.get("id"),
                }).execute()
                st.success(t("Anwesenheit gespeichert.", "Attendance saved."))
                st.rerun()
            except Exception as e:
                st.error(t("Konnte Anwesenheit nicht speichern.", "Could not save attendance.") + f" ({e})")
