import streamlit as st, uuid
from _auth import require_login, is_staff, supa
prof = require_login()
st.title("Dateien")

area = st.selectbox("Bereich", ["team","coaches","staff"])
if area in ("coaches","staff") and not is_staff(prof):
    st.warning("Kein Zugriff.")
else:
    file = st.file_uploader("Datei hochladen")
    if file and is_staff(prof):
        path = f"{uuid.uuid4()}_{file.name}"
        supa().storage.from_(area).upload(path, file.getvalue())
        supa().table("files_index").insert({"area":area,"path":path,"uploaded_by":prof["id"]}).execute()
        st.success("Datei hochgeladen.")
    items = supa().table("files_index").select("*").eq("area",area).order("created_at", desc=True).execute().data
    for it in items:
        st.write(f"• {it['path']} — {it['created_at']}")
