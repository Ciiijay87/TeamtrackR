import streamlit as st
from datetime import datetime, timedelta
from _data import list_events, create_event, update_event, delete_event, fmt_dt

st.set_page_config(page_title="Kalender", page_icon="📅", layout="wide")
st.title("📅 Kalender")

# --------- Event-Liste (links) ---------
with st.sidebar:
    st.header("Neues Event")
    title = st.text_input("Titel")
    colA, colB = st.columns(2)
    with colA:
        start = st.datetime_input("Start", value=datetime.now()+timedelta(hours=1))
    with colB:
        end = st.datetime_input("Ende", value=datetime.now()+timedelta(hours=2))
    location = st.text_input("Ort", value="")
    notes = st.text_area("Beschreibung", value="", height=80)
    if st.button("Event anlegen"):
        if not title:
            st.error("Titel fehlt.")
        else:
            payload = {
                "title": title,
                "start": start.isoformat(),
                "end": end.isoformat(),
                "location": location,
                "notes": notes
            }
            try:
                create_event(payload)
                st.success("Event angelegt.")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Fehler beim Anlegen: {e}")

events = list_events(200)
if not events:
    st.info("Noch keine Termine vorhanden. Lege links ein neues Event an.")
else:
    st.subheader("Termine")
    for ev in events:
        with st.expander(f'{ev.get("title","(ohne Titel)")} – {fmt_dt(ev.get("start"))}'):
            st.write(f"**Start:** {fmt_dt(ev.get('start'))}")
            st.write(f"**Ende:** {fmt_dt(ev.get('end'))}")
            if ev.get("location"): st.write(f"**Ort:** {ev['location']}")
            if ev.get("notes"): st.write(ev["notes"])

            # Edit
            with st.popover("✏️ Bearbeiten"):
                nt = st.text_input("Titel", value=ev.get("title",""), key=f"t_{ev['id']}")
                col1, col2 = st.columns(2)
                with col1:
                    ns = st.datetime_input("Start", value=datetime.fromisoformat(ev["start"].replace("Z","+00:00")), key=f"s_{ev['id']}")
                with col2:
                    ne = st.datetime_input("Ende", value=datetime.fromisoformat(ev["end"].replace("Z","+00:00")), key=f"e_{ev['id']}")
                nl = st.text_input("Ort", value=ev.get("location",""), key=f"l_{ev['id']}")
                nn = st.text_area("Beschreibung", value=ev.get("notes",""), key=f"n_{ev['id']}")
                if st.button("Speichern", key=f"u_{ev['id']}"):
                    try:
                        update_event(ev["id"], {
                            "title": nt, "start": ns.isoformat(), "end": ne.isoformat(),
                            "location": nl, "notes": nn
                        })
                        st.success("Gespeichert.")
                        st.experimental_rerun()
                    except Exception as e:
                        st.error(f"Fehler: {e}")
            # Delete
            if st.button("🗑️ Löschen", key=f"d_{ev['id']}"):
                try:
                    delete_event(ev["id"])
                    st.success("Gelöscht.")
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"Fehler: {e}")
