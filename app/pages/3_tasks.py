import streamlit as st
from datetime import datetime, timedelta
from _i18n import t, lang_selector
from _auth import supa, current_profile

st.set_page_config(page_title="Tasks", page_icon="📝", layout="wide")
lang_selector()

st.title("Tasks")

prof = current_profile()
if not prof:
    st.warning(t("Bitte einloggen.", "Please log in."))
    st.stop()

def is_staff_like(p: dict) -> bool:
    role = (p or {}).get("role", "player")
    return role in ["headcoach", "team_manager", "coach", "staff", "admin", "oc", "dc"]

# Liste
st.subheader(t("Offene Aufgaben", "Open tasks"))
try:
    res = supa().table("tasks").select("*").order("due_at", desc=False).limit(200).execute()
    rows = res.data or []
    if not rows:
        st.info(t("Noch keine Tasks.", "No tasks yet."))
    else:
        for tsk in rows:
            due = tsk.get("due_at")
            scope = tsk.get("scope", "team")
            st.markdown(f"**{tsk.get('title','—')}** — {tsk.get('description','')}  \n"
                        f"🗓 {due} • 🏷 {scope}")
except Exception as e:
    st.info(t("Tabelle 'tasks' nicht gefunden oder keine Leserechte.", "Table 'tasks' missing or no read access.") + f" ({e})")

# Neu anlegen (Staff)
if is_staff_like(prof):
    st.divider()
    st.subheader(t("Neuer Task", "New task"))
    with st.form("new_task"):
        title = st.text_input(t("Titel", "Title"))
        desc  = st.text_area(t("Beschreibung", "Description"))
        due   = st.datetime_input(t("Fällig (YYYY-MM-DD HH:MM)", "Due (YYYY-MM-DD HH:MM)"),
                                  value=datetime.now()+timedelta(days=1))
        scope = st.selectbox(t("Bereich", "Scope"), ["team", "staff"])
        submit = st.form_submit_button(t("Speichern", "Save"))
        if submit:
            try:
                supa().table("tasks").insert({
                    "title": title,
                    "description": desc,
                    "due_at": due.isoformat(),
                    "scope": scope,
                    "created_by": prof.get("id"),
                }).execute()
                st.success(t("Task gespeichert.", "Task saved."))
                st.rerun()
            except Exception as e:
                st.error(t("Konnte Task nicht speichern.", "Could not save task.") + f" ({e})")
