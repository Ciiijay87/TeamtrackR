import streamlit as st
from _data import list_events, list_players, get_attendance, set_attendance, attendance_summary

st.set_page_config(page_title="Anwesenheit", page_icon="✅", layout="wide")
st.title("✅ Anwesenheit")

# --- Event auswählen ---
events = list_events(200)
event_choices = {f'{e.get("title","(ohne Titel)")} – {e.get("start","")[:16]}': e["id"] for e in events}
if not event_choices:
    st.info("Kein Event vorhanden. Lege zuerst im Kalender ein Event an.")
    st.stop()

selected_label = st.selectbox("Event wählen", options=list(event_choices.keys()))
event_id = event_choices[selected_label]

# --- Unit-Filter ---
unit = st.selectbox("Unit", options=["Alle","Offense","Defense","ST"], index=0)

# --- Roster laden ---
players = list_players(None if unit=="Alle" else unit)
att = get_attendance(event_id)

# --- Farblogik für Status ---
def badge(label, color):
    st.markdown(f"""<span style="background:{color};color:white;padding:4px 8px;border-radius:8px;">{label}</span>""",
                unsafe_allow_html=True)

st.subheader("Check-in")
cols = st.columns([2,1,1,1,1])
cols[0].markdown("**Spieler**")
cols[1].markdown("**Da**")
cols[2].markdown("**Zu spät**")
cols[3].markdown("**Entschuldigt**")
cols[4].markdown("**Fehlt**")

for p in players:
    s = att.get(p["id"], {}).get("status")
    with st.container(border=True):
        c0, c1, c2, c3, c4 = st.columns([2,1,1,1,1])
        c0.write(p["display"])
        if c1.button("🟩", key=f"da_{p['id']}"):
            set_attendance(event_id, p["id"], "da")
            st.experimental_rerun()
        if c2.button("🟧", key=f"zs_{p['id']}"):
            set_attendance(event_id, p["id"], "zu_spaet")
            st.experimental_rerun()
        if c3.button("🟦", key=f"en_{p['id']}"):
            set_attendance(event_id, p["id"], "entschuldigt")
            st.experimental_rerun()
        if c4.button("🟥", key=f"fe_{p['id']}"):
            set_attendance(event_id, p["id"], "fehlt")
            st.experimental_rerun()
        if s:
            c0.caption(f"Aktuell: {s}")

# --- Zusammenfassung ---
st.divider()
st.subheader("Auswertung (Event)")
sumy = attendance_summary(event_id)
cA, cB, cC, cD, cE = st.columns(5)
cA.metric("Erfasst", sumy["total"])
cB.metric("Da", sumy["by_status"].get("da",0))
cC.metric("Zu spät", sumy["by_status"].get("zu_spaet",0))
cD.metric("Entschuldigt", sumy["by_status"].get("entschuldigt",0))
cE.metric("Fehlt", sumy["by_status"].get("fehlt",0))
st.caption("Score-Basis: Da=100, Zu spät=90, Entschuldigt=20, Fehlt=0")
