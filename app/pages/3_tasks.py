import streamlit as st
from datetime import datetime, timedelta
from _auth import require_login, is_staff
from data import list_tasks, create_task

st.set_page_config(page_title="Tasks", page_icon="✅", layout="wide")
prof = require_login()

st.title("Tasks")

# Offene Aufgaben
st.subheader("Offene Aufgaben")
tasks = list_tasks()
if not tasks:
    st.info("Keine Aufgaben vorhanden.")
else:
    nice = []
    for t in tasks:
        nice.append({
            "Titel": t.get("title"),
            "Beschreibung": t.get("description"),
            "Fällig": t.get("due"),
            "Bereich": t.get("scope"),
        })
    st.dataframe(nice, use_container_width=True)

st.divider()
st.subheader("Neuer Task")

if not is_staff(prof):
    st.info("Nur Staff (HC/TM/Coach/DC/OC/Staff) kann Tasks anlegen.")
else:
    with st.form("new_task"):
        ttl = st.text_input("Titel")
        desc = st.text_area("Beschreibung")
        due = st.datetime_input("Fällig (YYYY-MM-DD HH:MM)", value=datetime.now() + timedelta(days=1))
        scope = st.selectbox("Bereich", ["team", "staff", "offense", "defense", "special"])
        submit = st.form_submit_button("Speichern")
        if submit:
            if not ttl.strip():
                st.error("Titel darf nicht leer sein.")
            else:
                ok = create_task(ttl.strip(), desc.strip(), due, scope)
                if ok:
                    st.success("Task gespeichert.")
                    st.rerun()
                else:
                    st.error("Konnte Task nicht speichern (prüfe DB-Spalten).")
