import streamlit as st
from _auth import require_login, is_staff, supa
prof = require_login()
st.title("Ankündigungen")

tab_list, tab_new = st.tabs(["Übersicht","Neu"])

with tab_list:
    anns = supa().table("announcements").select("*").order("created_at", desc=True).execute().data
    for a in anns:
        st.write(f"**{a['title']}** — {a['created_at']}")
        st.caption(a["content"])

with tab_new:
    if is_staff(prof):
        title = st.text_input("Titel")
        content = st.text_area("Text")
        audience = st.selectbox("Zielgruppe", ["team","staff"])
        if st.button("Posten"):
            supa().table("announcements").insert({"title":title,"content":content,"audience":audience,"created_by":prof["id"]}).execute()
            st.success("Ankündigung erstellt."); st.experimental_rerun()
    else:
        st.info("Nur Staff kann posten.")
