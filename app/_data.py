# app/_data.py
from datetime import datetime
from typing import List, Dict, Any, Optional
import pandas as pd
from supabase import Client
import streamlit as st
from _auth import supa

# -------- EVENTS ----------
def create_event(title: str, start: datetime, end: datetime,
                 kind: str, visibility: str, notes: str) -> None:
    supa().table("events").insert({
        "title": title,
        "start": start.isoformat(),
        "end": end.isoformat(),
        "kind": kind,
        "visibility": visibility,
        "notes": notes
    }).execute()

def list_events(limit: int = 200) -> List[Dict[str, Any]]:
    res = supa().table("events").select("*").order("start", desc=False).limit(limit).execute()
    return res.data or []

# -------- TASKS ----------
def create_task(title: str, desc: str, due_at: Optional[datetime], audience: str, created_by: str) -> None:
    payload = {
        "title": title,
        "description": desc,
        "audience": audience,
        "created_by": created_by,
        "status": "open",
    }
    if due_at:
        payload["due_at"] = due_at.isoformat()
    supa().table("tasks").insert(payload).execute()

def list_tasks(audience: Optional[str] = None) -> pd.DataFrame:
    query = supa().table("tasks").select("*").order("created_at", desc=True)
    if audience:
        query = query.eq("audience", audience)
    res = query.execute()
    df = pd.DataFrame(res.data or [])
    if not df.empty and "due_at" in df.columns:
        df["due_at"] = pd.to_datetime(df["due_at"], errors="coerce")
    return df

# -------- ROSTER ----------
def roster_df() -> pd.DataFrame:
    res = supa().table("roster").select("*").order("last_name", desc=False).execute()
    return pd.DataFrame(res.data or [])

# -------- ATTENDANCE ----------
ATT_WEIGHTS = {
    "present": 1.00,
    "late": 0.75,
    "excused": 0.25,
    "absent": 0.00,
}

def save_attendance(event_id: str, player_id: str, status: str) -> None:
    supa().table("attendance").upsert({
        "event_id": event_id,
        "player_id": player_id,
        "status": status
    }, on_conflict="event_id,player_id").execute()

def load_attendance(event_id: str) -> pd.DataFrame:
    res = supa().table("attendance").select("*").eq("event_id", event_id).execute()
    return pd.DataFrame(res.data or [])
