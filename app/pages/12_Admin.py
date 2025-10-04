import streamlit as st
from _auth import require_login, is_admin, supa

st.set_page_config(page_title="Admin • TeamtrackR", page_icon="🛠️", layout="wide")

st.title("🛠️ Admin • Benutzerverwaltung")
st.caption("Nur Headcoach / Team Manager")

prof = require_login()
if not is_admin(prof):
    st.error("Kein Zugriff (nur Headcoach/Team Manager).")
    st.stop()

db = supa()
rows = db.table("profiles").select("id, email, display_name, role, approved").order("email").execute().data or []

if not rows:
    st.info("Noch keine Benutzer vorhanden.")
else:
    for r in rows:
        with st.container(border=True):
            c1, c2, c3, c4, c5 = st.columns([3,2,1.4,1.2,1.2])
            c1.write(f"**{r.get('display_name') or '—'}**\n{r.get('email') or '—'}")
            role = c2.selectbox(
                "Rolle",
                options=["player","staff","coach","team_manager","headcoach"],
                index=["player","staff","coach","team_manager","headcoach"].index(r.get("role") or "player"),
                key=f"role_{r['id']}"
            )
            appr = c3.toggle("Freigeschaltet", value=bool(r.get("approved")), key=f"app_{r['id']}")
            if c4.button("💾 Speichern", key=f"save_{r['id']}", use_container_width=True):
                db.table("profiles").update({"role": role, "approved": appr}).eq("id", r["id"]).execute()
                st.success("Gespeichert."); st.rerun()
            if c5.button("🗑️ Löschen", key=f"del_{r['id']}", use_container_width=True):
                db.table("profiles").delete().eq("id", r["id"]).execute()
                st.warning("Benutzer gelöscht."); st.rerun()
