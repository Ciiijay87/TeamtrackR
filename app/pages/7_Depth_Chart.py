import streamlit as st
from _auth import require_login, is_admin
from _auth import supa
import pandas as pd

st.set_page_config(page_title="Depth Chart", page_icon="📊", layout="wide")
prof = require_login()

# Schreibrecht: HC/TM/OC/DC
def can_write(p: dict) -> bool:
    return p.get("role") in ("headcoach","team_manager","oc","dc")

write_allowed = can_write(prof)

st.title("📊 Depth Chart")

# Units + Positions (frei erweiterbar)
DEFAULT_UNITS = ["Offense", "Defense", "ST"]
DEFAULT_POSITIONS = {
    "Offense": ["QB","RB","FB","WR","TE","LT","LG","C","RG","RT","Slot","H-Back"],
    "Defense": ["NT","DT","DE","SAM","MIKE","WILL","LCB","RCB","FS","SS","WS","STAR","NICKEL"],
    "ST":      ["K","P","LS","H","KR","PR","Gunner"]
}

# Laden Roster
roster = supa().table("roster").select("id, first_name, last_name, number, position, status").execute().data or []
players = [
    {"id": r["id"], "label": f'{r.get("number") or ""} {r.get("first_name","")} {r.get("last_name","")}'.strip()}
    for r in roster
]

# Auswahl
unit = st.selectbox("Unit", DEFAULT_UNITS, index=1)  # Default Defense
pos_list = DEFAULT_POSITIONS.get(unit, [])
position = st.selectbox("Position", pos_list + ["(eigene Bezeichnung)"])
if position == "(eigene Bezeichnung)":
    position = st.text_input("Eigene Positionsbezeichnung", placeholder="z.B. Weakside Safety (WS)")

st.markdown("**Slots**: 1=Starter, 2=Backup1, 3=Backup2, ...")

# Bestehenden Chart laden
existing = supa().table("depth_chart") \
    .select("id, unit, position, slot, player_id") \
    .eq("unit", unit).eq("position", position).order("slot", desc=False).execute().data or []

# Darstellung + Edit
max_slots = st.slider("Anzahl Slots", 1, 6, max(len(existing), 3))
slot_cols = st.columns(2)
left, right = slot_cols

def player_label(pid):
    for p in players:
        if p["id"] == pid:
            return p["label"]
    return "—"

current_rows = {row["slot"]: row for row in existing}
new_assignments = {}

for s in range(1, max_slots + 1):
    default_pid = current_rows.get(s, {}).get("player_id")
    default_name = player_label(default_pid)
    with (left if s % 2 == 1 else right):
        st.write(f"**Slot {s}**")
        if write_allowed:
            selected = st.selectbox(
                "Spieler wählen",
                ["—"] + [p["label"] for p in players],
                index=(["—"] + [p["label"] for p in players]).index(default_name) if default_name in ["—"] + [p["label"] for p in players] else 0,
                key=f"slot_{s}"
            )
            new_assignments[s] = next((p["id"] for p in players if p["label"] == selected), None)
        else:
            st.write(default_name or "—")

if write_allowed:
    if st.button("💾 Speichern", type="primary"):
        try:
            # Upsert je Slot
            upserts = []
            for s in range(1, max_slots + 1):
                pid = new_assignments.get(s)
                # leeren Slot entfernen
                if not pid:
                    # ggf. vorhandene Zeile löschen
                    if s in current_rows:
                        supa().table("depth_chart").delete().eq("id", current_rows[s]["id"]).execute()
                    continue
                row = {
                    "unit": unit,
                    "position": position,
                    "slot": s,
                    "player_id": pid,
                    "updated_by": prof["id"]
                }
                upserts.append(row)

            if upserts:
                supa().table("depth_chart").upsert(upserts, on_conflict="unit,position,slot").execute()
            st.success("Depth Chart gespeichert.")
            st.rerun()
        except Exception as e:
            st.error(f"Fehler beim Speichern: {e}")
else:
    st.info("Nur Headcoach, Team Manager, OC oder DC dürfen den Depth Chart bearbeiten.")

st.divider()
st.subheader(f"Aktuelle Zuordnung – {unit} / {position}")
df = pd.DataFrame([{
    "Slot": r["slot"],
    "Spieler": player_label(r["player_id"])
} for r in existing]).sort_values("Slot")
st.dataframe(df, use_container_width=True, hide_index=True)
