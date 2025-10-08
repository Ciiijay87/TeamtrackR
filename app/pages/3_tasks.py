import streamlit as st
from _auth import require_login, current_profile, supa, is_staff

st.set_page_config(page_title="Tasks")
st.header("Tasks")

require_login()
prof = current_profile()
if not prof.get("approved"):
    st.warning("Dein Zugang ist noch nicht freigeschaltet. Warte auf Freigabe durch HC/TM.")
    st.stop()

st.subheader("Neue Task")
title = st.text_input("Titel")
descr = st.text_area("Beschreibung")
due = st.text_input("Fällig (YYYY-MM-DD HH:MM)")
scope = st.selectbox("Bereich", ["staff","players","all"])

if st.button("Speichern"):
    supa().table("tasks").insert({
        "title": title,
        "description": descr,
        "due_at": due or None,
        "scope": scope,
        "created_by": prof["id"]
    }).execute()
    st.success("Task gespeichert.")

st.subheader("Offene Tasks")
rows = supa().table("tasks").select("*").order("created_at", desc=True).execute().data or []
for r in rows:
    with st.expander(f"{r['title']}  •  Bereich: {r['scope']}"):
        st.write(r.get("description") or "")
        st.caption(f"Fällig: {r.get('due_at')}")
