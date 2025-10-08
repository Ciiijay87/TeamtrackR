# app/pages/2_Attendance.py
import streamlit as st
import pandas as pd
from _auth import require_login
from _data import list_events, roster_df, load_attendance, save_attendance, ATT_WEIGHTS

st.set_page_config(page_title="Anwesenheit", layout="wide")
prof = require_login()

st.title("✅ Anwesenheit")

# Event wählen
events = list_events(200)
if not events:
    st.info("Noch keine Events – lege zuerst eins im Kalender an.")
    st.stop()

ev_map = {f"{e['title']} | {e['start']}": e for e in events}
ev_key = st.selectbox("Event", list(ev_map.keys()))
ev = ev_map[ev_key]
event_id = ev["id"]

# Roster laden
r = roster_df()
if r.empty:
    st.info("Noch kein Roster eingepflegt.")
    st.stop()

# Bisherige Attendance laden
att = load_attendance(event_id)
status_by_player = {row["player_id"]: row["status"] for _, row in att.iterrows()}

# Status-Auswahl pro Spieler
status_options = {
    "Anwesend (grün)": "present",
    "Verspätet (orange)": "late",
    "Entschuldigt (blau)": "excused",
    "Abwesend (rot)": "absent",
}

st.write("Status je Spieler setzen und unten 'Speichern' klicken.")
chosen = {}
for _, row in r.iterrows():
    pid = row["id"]
    preset = status_by_player.get(pid, "absent")
    label = f"{row.get('number','')} {row.get('first_name','')} {row.get('last_name','')}"
    val = st.selectbox(label, list(status_options.keys()),
                       index=list(status_options.values()).index(preset),
                       key=f"att_{pid}")
    chosen[pid] = status_options[val]

if st.button("Speichern"):
    try:
        for pid, stt in chosen.items():
            save_attendance(event_id, str(pid), stt)
        st.success("Anwesenheit gespeichert.")
    except Exception as e:
        st.error(f"Fehler: {e}")

# Ampel-Ansicht (Styling)
def color_status(s):
    m = {"present":"background-color: #d9f2d9",   # grün
         "late":"background-color: #ffe8cc",      # orange
         "excused":"background-color: #dbe9ff",   # blau
         "absent":"background-color: #ffd6d6"}    # rot
    return [m.get(v, "") for v in s]

att = load_attendance(event_id)
df = r[["id","first_name","last_name","position","number"]].copy()
df = df.rename(columns={"id":"player_id"})
df = df.merge(att, on="player_id", how="left")
df["status"] = df["status"].fillna("absent")
df["Score"] = df["status"].map(ATT_WEIGHTS).round(2)

styled = df[["number","first_name","last_name","position","status","Score"]].style.apply(color_status, subset=["status"])
st.subheader("Übersicht (Ampel)")
st.dataframe(styled, use_container_width=True)
