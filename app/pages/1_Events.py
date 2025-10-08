import streamlit as st
from datetime import datetime, date, time, timedelta
from _auth import require_login, supa, is_staff
from _i18n import t

st.set_page_config(page_title="Kalender", page_icon="📅", layout="wide")
prof = require_login()

st.markdown("## 📅 Kalender")

is_staff_user = is_staff(prof)

# ---------- Formular "Neues Event" ----------
with st.sidebar:
    st.markdown("### Neues Event")
    title = st.text_input("Titel", "")
    d = st.date_input("Datum", value=date.today())
    start_t = st.time_input("Start", value=(datetime.now()+timedelta(hours=1)).time())
    end_t = st.time_input("Ende", value=(datetime.now()+timedelta(hours=2)).time())
    place = st.text_input("Ort", "")
    vis = st.selectbox("Sichtbarkeit", ["team", "staff"])  # simpel
    notes = st.text_area("Beschreibung", "")

    if is_staff_user and st.button("Speichern"):
        start = datetime.combine(d, start_t)
        end = datetime.combine(d, end_t)
        try:
            supa().table("events").insert({
                "title": title.strip(),
                "start": start.isoformat(),
                "end": end.isoformat(),
                "place": place.strip(),
                "visibility": vis,
                "notes": notes.strip()
            }).execute()
            st.success("Event gespeichert.")
            st.rerun()
        except Exception as e:
            st.error("Konnte Event nicht speichern.")
            st.exception(e)

# ---------- Liste der nächsten Events ----------
st.markdown("### Nächste Termine")
try:
    res = supa().table("events").select("*").order("start", desc=False).limit(50).execute()
    rows = res.data or []
    if not rows:
        st.info("Noch keine Events angelegt.")
    else:
        for ev in rows:
            with st.container(border=True):
                st.markdown(f"**{ev.get('title','(ohne Titel)')}**")
                st.caption(
                    f"{ev.get('start','?')} – {ev.get('end','?')} | {ev.get('place','')}"
                    f" | Sichtbarkeit: {ev.get('visibility','team')}"
                )
                if ev.get("notes"):
                    st.write(ev["notes"])
except Exception as e:
    st.error("Konnte Events nicht laden (Policy/Schema?).")
    st.exception(e)
