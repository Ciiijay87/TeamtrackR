import streamlit as st
from datetime import datetime
from _auth import require_login, supa, is_staff
from _i18n import t

st.set_page_config(page_title="Anwesenheit", page_icon="✅", layout="wide")
prof = require_login()
staff = is_staff(prof)

st.markdown("## ✅ Anwesenheit")

# Letztes/nächstes Event holen (einfach: das nächste in der Zukunft, sonst letztes)
def get_target_event():
    try:
        # nächstes in Zukunft
        r = supa().table("events").select("*").gte("start", datetime.utcnow().isoformat()) \
            .order("start", desc=False).limit(1).execute()
        if r.data:
            return r.data[0]
        # sonst letztes Vergangenes
        r = supa().table("events").select("*").lt("start", datetime.utcnow().isoformat()) \
            .order("start", desc=True).limit(1).execute()
        if r.data:
            return r.data[0]
    except Exception:
        pass
    return None

event = get_target_event()
if not event:
    st.info("Kein Event gefunden. Lege im Kalender eines an.")
    st.stop()

st.write(f"**Event:** {event['title']} – {event['start']} @ {event.get('place','')}")

# Roster laden
try:
    res_roster = supa().table("roster").select("id, first_name, last_name, position").order("last_name").execute()
    roster = res_roster.data or []
except Exception as e:
    st.error("Konnte Roster nicht laden (Policy/Schema?).")
    st.exception(e)
    st.stop()

# Bisherige Anwesenheit lesen
att_map = {}
try:
    r = supa().table("attendance").select("*").eq("event_id", event["id"]).execute()
    for row in (r.data or []):
        att_map[row["player_id"]] = row
except Exception:
    pass

status_opts = {
    "da": "✅ da",
    "late": "⏰ zu spät",
    "excused": "📝 entschuldigt",
    "absent": "❌ fehlt",
}

if staff:
    st.markdown("### Check-in")
    for p in roster:
        pid = p["id"]
        name = f"{p.get('first_name','')} {p.get('last_name','')}".strip()
        old = att_map.get(pid, {})
        col1, col2 = st.columns([2, 1])
        with col1:
            st.write(name, f"({p.get('position','')})")
        with col2:
            new_status = st.selectbox(
                "Status", list(status_opts.keys()),
                index=list(status_opts.keys()).index(old.get("status", "absent")),
                key=f"status_{pid}",
                format_func=lambda k: status_opts[k]
            )
        # Speichern pro Zeile
        if st.button("Speichern", key=f"save_{pid}"):
            try:
                supa().table("attendance").upsert({
                    "event_id": event["id"],
                    "player_id": pid,
                    "status": new_status
                }).execute()
                st.success("Gespeichert.")
                st.rerun()
            except Exception as e:
                st.error("Konnte Status nicht speichern.")
                st.exception(e)
else:
    st.info("Nur Staff kann Anwesenheit eintragen.")
