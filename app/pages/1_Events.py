# app/pages/1_Events.py
import streamlit as st
from datetime import datetime, timedelta, time
from _auth import require_login
from _data import create_event, list_events

st.set_page_config(page_title="Kalender", layout="wide")
prof = require_login()

st.title("Kalender")

with st.form("new_event"):
    st.subheader("Neues Event")
    title = st.text_input("Titel")
    kind = st.selectbox("Typ", ["training", "game", "meeting", "travel", "tryout", "other"])
    visibility = st.selectbox("Sichtbarkeit", ["team", "staff"])
    notes = st.text_area("Beschreibung / Notizen", height=100)

    d = st.date_input("Datum", value=datetime.now().date())
    start_t = st.time_input("Start", value=(datetime.now()+timedelta(hours=1)).time())
    end_t = st.time_input("Ende", value=(datetime.now()+timedelta(hours=2)).time())

    submitted = st.form_submit_button("Speichern")
    if submitted:
        start = datetime.combine(d, start_t)
        end = datetime.combine(d, end_t)
        try:
            create_event(title, start, end, kind, visibility, notes)
            st.success("Event gespeichert.")
        except Exception as e:
            st.error(f"Fehler beim Speichern: {e}")

st.divider()
st.subheader("Alle Events (nächste / letzte)")

events = list_events(200)
if not events:
    st.info("Noch keine Events.")
else:
    from pandas import DataFrame, to_datetime
    import pandas as pd
    df = DataFrame(events)
    for col in ("start","end"):
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce").dt.tz_localize(None)
    show = df[["title","kind","visibility","start","end","notes"]]
    st.dataframe(show, use_container_width=True, hide_index=True)
