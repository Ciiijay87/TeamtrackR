import streamlit as st
from datetime import datetime, timedelta
from _auth import require_login, supa, is_staff

st.set_page_config(page_title="Tasks", page_icon="🧾", layout="wide")
prof = require_login()
staff = is_staff(prof)

st.markdown("## 🧾 Tasks")

# Formular
with st.container(border=True):
    st.markdown("### Neu")
    title = st.text_input("Titel")
    desc = st.text_area("Beschreibung")
    due_date = st.date_input("Fällig (YYYY-MM-DD)", value=datetime.utcnow().date() + timedelta(days=1))
    due_time = st.time_input("Uhrzeit", value=datetime.utcnow().time().replace(second=0, microsecond=0))
    area = st.selectbox("Bereich", ["team", "staff"])

    if staff and st.button("Speichern"):
        try:
            dt = datetime.combine(due_date, due_time)
            supa().table("tasks").insert({
                "title": title.strip(),
                "description": desc.strip(),
                "due": dt.isoformat(),
                "area": area
            }).execute()
            st.success("Task gespeichert.")
            st.rerun()   # <— wichtig: ersetzt experimental_rerun
        except Exception as e:
            st.error("Konnte Task nicht speichern.")
            st.exception(e)

# Liste
st.markdown("### Offene Tasks")
try:
    r = supa().table("tasks").select("*").order("due", desc=False).limit(200).execute()
    rows = r.data or []
    if not rows:
        st.info("Keine Tasks vorhanden.")
    else:
        for tsk in rows:
            with st.container(border=True):
                st.markdown(f"**{tsk.get('title','(ohne Titel)')}** – {tsk.get('area','')}")
                st.caption(f"Fällig: {tsk.get('due','?')}")
                if tsk.get("description"):
                    st.write(tsk["description"])
except Exception as e:
    st.error("Konnte Tasks nicht laden.")
    st.exception(e)
