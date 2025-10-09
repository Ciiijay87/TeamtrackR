import streamlit as st
from datetime import datetime, timedelta
from _auth import require_login, is_staff
from data import list_events, create_event

st.set_page_config(page_title="Kalender", page_icon="📅", layout="wide")
prof = require_login()

st.title("Kalender")

# Liste bestehender Termine
events = list_events()
if not events:
    st.info("Noch keine Termine vorhanden.")
else:
    st.dataframe(
        [{k: v for k, v in e.items() if k in ("title", "start", "end", "location")} for e in events],
        use_container_width=True,
    )

st.divider()
st.subheader("Neues Event")

if not is_staff(prof):
    st.info("Nur Staff (HC/TM/Coach/DC/OC/Staff) kann Termine anlegen.")
else:
    with st.form("new_event"):
        title = st.text_input("Titel / Title")
        start = st.datetime_input("Start", value=datetime.now() + timedelta(hours=1))
        end = st.datetime_input("Ende (optional)", value=None)
        location = st.text_input("Ort (optional)")
        save = st.form_submit_button("Speichern")
        if save:
            ok = create_event(title.strip(), start, end, location.strip())
            if ok:
                st.success("Event gespeichert.")
                st.rerun()
            else:
                st.error("Konnte Event nicht speichern (prüfe DB-Spalten).")
