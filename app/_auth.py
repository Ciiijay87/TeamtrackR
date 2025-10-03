import streamlit as st
from supabase import create_client, Client
from typing import Optional
import functools

@functools.lru_cache(maxsize=1)
def _client() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_ANON_KEY"]
    return create_client(url, key)

def supa() -> Client:
    return _client()

def get_session():
    return st.session_state.get("session")

def sign_in(email: str, password: str):
    res = supa().auth.sign_in_with_password({"email": email, "password": password})
    st.session_state["session"] = res.session
    return res

def sign_up(email: str, password: str, display_name: str):
    res = supa().auth.sign_up({
        "email": email, "password": password,
        "options": {"data": {"display_name": display_name}}
    })
    st.session_state["session"] = res.session
    return res

def sign_out():
    supa().auth.sign_out()
    st.session_state.pop("session", None)

def current_profile() -> Optional[dict]:
    s = get_session()
    if not s:
        return None
    uid = s.user.id
    data = supa().table("profiles").select("*").eq("id", uid).single().execute()
    return data.data

def require_login():
    prof = current_profile()
    if not prof:
        st.error("Bitte einloggen. / Please sign in.")
        st.stop()
    if not prof.get("approved", False):
        st.warning("Dein Zugang ist noch nicht freigeschaltet. Warte auf Freigabe durch HC/TM.")
        st.stop()
    return prof

def is_staff(prof: dict) -> bool:
    return prof.get("role") in ("coach","headcoach","team_manager","staff")
