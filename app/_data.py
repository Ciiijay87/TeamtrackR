from datetime import datetime
from typing import List, Dict, Optional, Any
from _auth import supa

# -------- EVENTS --------
def list_events(limit: int = 200) -> List[Dict]:
    try:
        res = (supa().table("events")
               .select("*")
               .order("start", desc=False)
               .limit(limit)
               .execute())
        return res.data or []
    except Exception:
        return []

def create_event(title: str, start: datetime, end: Optional[datetime], location: str) -> bool:
    try:
        payload = {"title": title, "start": start.isoformat()}
        if end:
            payload["end"] = end.isoformat()
        if location:
            payload["location"] = location
        supa().table("events").insert(payload).execute()
        return True
    except Exception:
        return False

# -------- TASKS --------
def list_tasks() -> List[Dict]:
    try:
        res = (supa().table("tasks")
               .select("*")
               .order("due", desc=False)
               .execute())
        return res.data or []
    except Exception:
        return []

def create_task(title: str, description: str, due: Optional[datetime], scope: str) -> bool:
    try:
        payload: Dict[str, Any] = {"title": title, "scope": scope}
        if description:
            payload["description"] = description
        if due:
            payload["due"] = due.isoformat()
        supa().table("tasks").insert(payload).execute()
        return True
    except Exception:
        return False
