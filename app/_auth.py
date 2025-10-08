import streamlit as st
from supabase import create_client, Client
from typing import Optional, Dict
import functools

# ---- Supabase Client aus Secrets ----
@functools.lru_cache(maxsize=1)
def _client() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_ANON_KEY"]
    return create_client(url, key)

def supa() -> Client:
    return _client()

# ---- Session Helpers ----
def get_session() -> Optional[Dict]:
    return st.session_state.get("session")

def require_login() -> Optional[Dict]:
    sess = get_session()
    if not sess:
        st.warning("Bitte einloggen.")
        st.stop()
    return sess

def is_staff(profile: Optional[Dict]) -> bool:
    if not profile: 
        return False
    return profile.get("role") in ("headcoach", "team_manager", "coach", "dc", "oc", "staff")

def is_admin(profile: Optional[Dict]) -> bool:
    if not profile:
        return False
    return profile.get("role") in ("headcoach", "team_manager")

# ---- Auth Flows ----
def sign_in(email: str, password: str) -> bool:
    res = supa().auth.sign_in_with_password({"email": email, "password": password})
    st.session_state["session"] = res.session
    return res.session is not None

def sign_out():
    supa().auth.sign_out()
    st.session_state.pop("session", None)
    st.rerun()

def sign_up(email: str, password: str, display_name: str) -> bool:
    res = supa().auth.sign_up(
        {
            "email": email,
            "password": password,
            "options": {"data": {"display_name": display_name}},
        }
    )
    # Profil anlegen (pending approval)
    user = res.user
    if user:
        supa().table("profiles").upsert({
            "id": user.id,
            "email": email,
            "display_name": display_name,
            "role": "player",
            "approved": False
        }).execute()
    return True

def current_profile() -> Optional[Dict]:
    sess = get_session()
    if not sess:
        return None
    uid = sess.user.id
    data = supa().table("profiles").select("*").eq("id", uid).single().execute()
    return data.data
