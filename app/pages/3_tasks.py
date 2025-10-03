import streamlit as st
from _auth import require_login, is_staff, supa
prof = require_login()
st.title("Tasks")

tab_list, tab_new = st.tabs(["Liste","Neu"])

with tab_list:
    tasks = supa().table("tasks").select("*").order("due_at").execute().data
    for t in tasks:
        scope = t["scope"]
        if scope=="staff" and not is_staff(prof): 
            continue
        st.write(f"**{t['title']}** — {t.get('due_at','')} — {t['status']} — [{scope}]")

with tab_new:
    if is_staff(prof):
        title = st.text_input("Titel")
        desc = st.text_area("Beschreibung")
        due = st.text_input("Fällig (YYYY-MM-DD HH:MM)")
        scope = st.selectbox("Bereich", ["team","staff"])
        if st.button("Speichern"):
            supa().table("tasks").insert({"title":title,"description":desc,"due_at":due,"scope":scope,"created_by":prof["id"]}).execute()
            st.success("Task gespeichert."); st.experimental_rerun()
    else:
        st.info("Nur Staff kann Tasks erstellen.")
