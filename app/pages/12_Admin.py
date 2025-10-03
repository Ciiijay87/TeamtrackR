import streamlit as st
from _auth import require_login, supa
prof = require_login()
st.title("Admin")

users = supa().table("profiles").select("*").execute().data
for u in users:
    st.write(f"{u['email']} — {u.get('role','?')} — {'✅' if u.get('approved') else '⏳'}")
    col1, col2 = st.columns(2)
    newrole = col1.selectbox("Rolle", ["player","coach","headcoach","team_manager","staff"], key=f"r{u['id']}", index=0)
    approved = col2.checkbox("Freigabe", value=u.get("approved"), key=f"a{u['id']}")
    if st.button("Speichern", key=f"s{u['id']}"):
        supa().table("profiles").update({"role":newrole,"approved":approved}).eq("id",u["id"]).execute()
        st.experimental_rerun()
