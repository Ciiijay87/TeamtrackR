from typing import List, Dict, Optional
from _auth import supa

# ---------- Events ----------
def get_upcoming_events(limit: int = 5) -> List[Dict]:
    q = supa().table("events").select("*").order("start_time", desc=False).limit(limit).execute()
    return q.data or []

def create_event(title: str, start_time: str, end_time: Optional[str], location: str, visibility: str, notes: str) -> None:
    supa().table("events").insert({
        "title": title,
        "start_time": start_time,
        "end_time": end_time,
        "location": location,
        "visibility": visibility,  # 'team' oder 'staff'
        "notes": notes
    }).execute()

# ---------- Roster ----------
def get_roster(active_only: bool = True) -> List[Dict]:
    q = supa().table("roster").select("id, first_name, last_name, position, number, status").execute()
    rows = q.data or []
    if active_only:
        rows = [r for r in rows if (r.get("status") or "").lower() in ("fit", "active", "")]
    return rows

# ---------- Attendance ----------
ATTENDANCE_VALUES = ["present", "late", "excused", "absent"]

def get_attendance(event_id: str) -> Dict[str, str]:
    q = supa().table("attendance").select("player_id, status").eq("event_id", event_id).execute()
    rows = q.data or []
    return {r["player_id"]: r["status"] for r in rows}

def set_attendance(event_id: str, player_id: str, status: str) -> None:
    if status not in ATTENDANCE_VALUES:
        status = "absent"
    supa().table("attendance").upsert({
        "event_id": event_id,
        "player_id": player_id,
        "status": status
    }, on_conflict="event_id,player_id").execute()

# ---------- Tasks ----------
def count_open_tasks() -> int:
    q = supa().table("tasks").select("id,status").neq("status", "done").execute()
    return len(q.data or [])

# ---------- Announcements ----------
def get_latest_announcements(limit: int = 3) -> List[Dict]:
    q = supa().table("announcements").select("*").order("created_at", desc=True).limit(limit).execute()
    return q.data or []
