import streamlit as st
from datetime import datetime, timedelta
from _i18n import t, lang_selector
from _auth import supa, current_profile

st.set_page_config(page_title="Events", page_icon="📅", layout="wide")
lang_selector()

st.title(t("Kalender", "Events"))

prof = current_profile()
if not prof:
    st.warning(t("Bitte einloggen.", "Please log in."))
    st.stop()

def can_create_events(p: dict) -> bool:
    role = (p or {}).get("role", "player")
    return role in ["headcoach", "team_manager", "coach", "staff", "admin", "oc", "dc"]

# Liste Events
st.subheader(t("Termine", "Upcoming events"))
try:
    res = supa().table("events").select("*").order("start", desc=False).limit(200).execute()
    rows = res.data or []
    if not rows:
        st.info(t("Noch keine Termine.", "No events yet."))
    else:
        for ev in rows:
            start = ev.get("start")
            end = ev.get("end")
            title = ev.get("title", "—")
            loc = ev.get("location", "")
            st.markdown(f"**{title}** — {start} → {end}  {('• ' + loc) if loc else ''}")
except Exception as e:
    st.info(t("Tabelle 'events' nicht gefunden oder keine Leserechte.", "Table 'events' missing or no read access.") + f" ({e})")

# Neues Event (nur Staff/Coach/HC/TM/OC/DC/Admin)
if can_create_events(prof):
    st.divider()
    st.subheader(t("Neues Event", "New event"))
    with st.form("new_event"):
        title = st.text_input("Titel / Title")
        start = st.datetime_input("Start", value=datetime.now()+timedelta(hours=1))
        end   = st.datetime_input("Ende / End", value=datetime.now()+timedelta(hours=2))
        loc   = st.text_input("Ort / Location", "")
        submit = st.form_submit_button(t("Speichern", "Save"))
        if submit:
            try:
                supa().table("events").insert({
                    "title": title,
                    "start": start.isoformat(),
                    "end": end.isoformat(),
                    "location": loc,
                    "created_by": prof.get("id"),
                }).execute()
                st.success(t("Event gespeichert.", "Event saved."))
                st.rerun()
            except Exception as e:
                st.error(t("Konnte Event nicht speichern.", "Could not save event.") + f" ({e})")
