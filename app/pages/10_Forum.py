import streamlit as st
from _auth import require_login, supa, is_staff
prof = require_login()
st.title("Forum")

threads = supa().table("forum_threads").select("*").order("created_at", desc=True).execute().data
for t in threads:
    st.subheader(t["title"])
    st.caption(f"von {t['created_by']} — {t['created_at']}")
    posts = supa().table("forum_posts").select("*").eq("thread_id", t["id"]).order("created_at").execute().data
    for p in posts:
        st.write(f"- {p['content']} ({p['created_by']})")
    newp = st.text_input("Antwort", key=f"p{t['id']}")
    if st.button("Posten", key=f"b{t['id']}"):
        supa().table("forum_posts").insert({"thread_id":t["id"],"content":newp,"created_by":prof["id"]}).execute()
        st.experimental_rerun()

if is_staff(prof):
    with st.form("newthread"):
        title = st.text_input("Neues Thema")
        aud = st.selectbox("Sichtbarkeit", ["team","staff"])
        ok = st.form_submit_button("Thread erstellen")
    if ok:
        supa().table("forum_threads").insert({"title":title,"audience":aud,"created_by":prof["id"]}).execute()
        st.experimental_rerun()
