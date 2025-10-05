import functools
from typing import List, Optional, Dict, Any
import streamlit as st
from supabase import create_client, Client
from datetime import datetime

# ---------- SUPABASE ----------
@functools.lru_cache(maxsize=1)
def supa() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_ANON_KEY"]
    return create_client(url, key)

# ---------- EVENTS ----------
def list_events(limit: int = 50) -> List[Dict[str, Any]]:
    res = supa().table("events").select("*").order("start", desc=False).limit(limit).execute()
    return res.data or []

def create_event(payload: Dict[str, Any]) -> Dict[str, Any]:
    res = supa().table("events").insert(payload).select("*").single().execute()
    return res.data

def update_event(event_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    res = supa().table("events").update(payload).eq("id", event_id).select("*").single().execute()
    return res.data

def delete_event(event_id: str) -> None:
    supa().table("events").delete().eq("id", event_id).execute()

# ---------- ROSTER ----------
# Falls ihr im Roster keine "unit"-Spalte habt, mappen wir sie grob aus "position".
_POS2UNIT = {
    "QB":"Offense","RB":"Offense","WR":"Offense","TE":"Offense","OL":"Offense","C":"Offense","G":"Offense","T":"Offense",
    "DL":"Defense","DE":"Defense","DT":"Defense","NT":"Defense","EDGE":"Defense","LB":"Defense","ILB":"Defense","OLB":"Defense",
    "DB":"Defense","CB":"Defense","LCB":"Defense","RCB":"Defense","S":"Defense","SS":"Defense","FS":"Defense","WS":"Defense",
    "K":"ST","P":"ST","LS":"ST","KR":"ST","PR":"ST"
}

def _infer_unit(position: Optional[str]) -> str:
    if not position:
        return "Offense"
    p = position.strip().upper()
    return _POS2UNIT.get(p, "Offense")

def list_players(unit_filter: Optional[str] = None) -> List[Dict[str, Any]]:
    # Wir holen Kernfelder; existieren manche nicht, liefert Supabase einfach None
    fields = "id, first_name, last_name, number, position, status"
    res = supa().table("roster").select(fields).order("last_name").order("first_name").execute()
    rows = res.data or []
    for r in rows:
        r["unit"] = r.get("unit") or _infer_unit(r.get("position"))
        r["display"] = f'{r.get("number") or ""} {r.get("first_name","")} {r.get("last_name","")}'.strip()
    if unit_filter:
        rows = [r for r in rows if r["unit"] == unit_filter]
    return rows

# ---------- ATTENDANCE ----------
# Status & Bewertung
ATTENDANCE_WEIGHTS = {"da":100, "zu_spaet":90, "entschuldigt":20, "fehlt":0}

def get_attendance(event_id: str) -> Dict[str, Dict[str, Any]]:
    """liefert Dict[player_id] -> {status, updated_at}"""
    res = supa().table("attendance").select("player_id,status,updated_at").eq("event_id", event_id).execute()
    out: Dict[str, Dict[str, Any]] = {}
    for row in (res.data or []):
        out[row["player_id"]] = {"status": row["status"], "updated_at": row.get("updated_at")}
    return out

def set_attendance(event_id: str, player_id: str, status: str) -> None:
    # Upsert per (event_id, player_id)
    payload = {"event_id": event_id, "player_id": player_id, "status": status}
    supa().table("attendance").upsert(payload, on_conflict="event_id,player_id").execute()

def attendance_summary(event_id: str) -> Dict[str, Any]:
    data = get_attendance(event_id)
    total = len(data)
    by_status = {"da":0,"zu_spaet":0,"entschuldigt":0,"fehlt":0}
    score = 0
    for v in data.values():
        s = v.get("status","fehlt")
        if s not in by_status: by_status[s] = 0
        by_status[s] += 1
        score += ATTENDANCE_WEIGHTS.get(s, 0)
    avg = round(score / max(1,total), 1) if total else 0
    return {"total": total, "by_status": by_status, "avg_score": avg}

# ---------- Kleine Helfer ----------
def fmt_dt(dt: Optional[str]) -> str:
    try:
        return datetime.fromisoformat(dt.replace("Z","+00:00")).strftime("%d.%m.%Y %H:%M")
    except Exception:
        return dt or ""
