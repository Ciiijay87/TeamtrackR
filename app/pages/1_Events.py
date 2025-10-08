import streamlit as st
from _auth import require_login, current_profile, is_staff, supa

st.set_page_config(page_title="Kalender")
st.header("Kalender")

sess = require_login()
prof = current_profile()
if not prof.get("approved"):
    st.warning("Dein Zugang ist noch nicht freigeschaltet. Warte auf Freigabe durch HC/TM.")
    st.stop()

# Liste Events
def list_events(limit=200):
    res = supa().table("events").select("*").order("start", desc=False).limit(limit).execute()
    return res.data or []

# Neues Event anlegen (nur Staff)
if is_staff(prof):
    st.subheader("Neues Event")
    title = st.text_input("Titel")
    start = st.datetime_input("Start")
    end = st.datetime_input("Ende")
    cat = st.selectbox("Kategorie", ["practice", "game", "meeting", "other"])
    if st.button("Speichern"):
        supa().table("events").insert({
            "title": title,
            "start": start.isoformat(),
            "end": end.isoformat(),
            "category": cat
        }).execute()
        st.success("Event gespeichert.")
        st.rerun()

st.subheader("Alle Events")
ev = list_events()
if not ev:
    st.info("Noch keine Events.")
else:
    for e in ev:
        with st.expander(f"{e.get('title')}  •  {e.get('start')}"):
            st.write(e)
