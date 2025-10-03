from typing import List
from ._auth import supa

def list_units() -> List[str]:
    return ["OL","WR","RB","TE","QB","DL","DB","LB","K","P"]

def get_events(limit=50):
    return supa().table("events").select("*").order("starts_at", desc=False).limit(limit).execute().data

def get_roster():
    return supa().table("roster").select("*").order("number", desc=False).execute().data

def set_attendance(event_id: int, player_id: str, status: str, checked_by: str):
    supa().table("attendance").upsert({
        "event_id": event_id,
        "player_id": player_id,
        "status": status,
        "checked_by": checked_by
    }).execute()

def list_attendance(event_id: int):
    return supa().table("attendance").select("*").eq("event_id", event_id).execute().data

def list_categories():
    return supa().table("event_categories").select("*").order("name").execute().data
