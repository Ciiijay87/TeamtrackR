# app/pages/3_tasks.py
import streamlit as st
from datetime import datetime
from _auth import require_login
from _data import create_task, list_tasks

st.set_page_config(page_title="Tasks", layout="wide")
prof = require_login()

st.title("Tasks")

with st.form("task_form"):
    title = st.text_input("Titel")
    desc = st.text_area("Beschreibung", height=120)
    due = st.date_input("Fälligkeitsdatum (optional)")
    due_time = st.time_input("Fälligkeitszeit (optional)")
    audience = st.selectbox("Bereich", ["team", "staff"])
    submit = st.form_submit_button("Speichern")
    if submit:
        due_at = None
        try:
            if due and due_time:
                due_at = datetime.combine(due, due_time)
        except Exception:
            pass
        try:
            create_task(title, desc, due_at, audience, prof["id"])
            st.success("Task gespeichert.")
        except Exception as e:
            st.error(f"Fehler: {e}")

st.divider()
st.subheader("Liste")
df = list_tasks()
if df.empty:
    st.info("Noch keine Tasks.")
else:
    st.dataframe(df[["audience","title","description","status","due_at"]], use_container_width=True, hide_index=True)
