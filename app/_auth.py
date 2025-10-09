import streamlit as st
from supabase import create_client, Client
from typing import Optional, Any, Dict
import functools

# ---------- Supabase Client ----------
@functools.lru_cache(maxsize=1)
def _client() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_ANON_KEY"]
    return create_client(url, key)

def supa() -> Client:
    return _client()

# ---------- Session ----------
def get_session():
    return st.session_state.get("session")

def sign_in(email: str, password: str) -> bool:
    try:
        res = supa().auth.sign_in_with_password({"email": email, "password": password})
        st.session_state["session"] = res.session
        return True
    except Exception as e:
        st.error("Login fehlgeschlagen. Prüfe E-Mail/Passwort oder E-Mail-Bestätigung.")
        return False

def sign_up(email: str, password: str, display_name: str) -> bool:
    try:
        supa().auth.sign_up({
            "email": email,
            "password": password,
            "options": {"data": {"display_name": display_name}},
        })
        st.success("Registriert. Bitte bestätige deine E-Mail.")
        return True
    except Exception:
        st.error("Registrierung fehlgeschlagen.")
        return False

def sign_out():
    try:
        supa().auth.sign_out()
    finally:
        st.session_state.pop("session", None)

# ---------- Helpers ----------
def _safe_get(obj: Any, key: str, default=None):
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    try:
        return getattr(obj, key)
    except Exception:
        return default

# ---------- Profile ----------
def current_profile() -> Optional[Dict]:
    s = get_session()
    if not s or not s.user:
        return None
    uid = s.user.id
    try:
        res = supa().table("profiles").select("*").eq("id", uid).single().execute()
        return res.data if isinstance(res.data, dict) else None
    except Exception:
        return None

def require_login() -> Dict:
    prof = current_profile()
    if not prof:
        st.warning("Bitte einloggen.")
        st.stop()
    if not _safe_get(prof, "approved", False):
        st.warning("Dein Zugang ist noch nicht freigeschaltet.")
        st.stop()
    return prof

# ---------- Roles ----------
COACH_ROLES = ("headcoach", "team_manager", "coach", "dc", "oc", "staff")

def role_of(prof: Optional[Dict]) -> Optional[str]:
    return _safe_get(prof, "role")

def is_admin(prof: Optional[Dict]) -> bool:
    return role_of(prof) in ("headcoach", "team_manager")

def is_staff(prof: Optional[Dict]) -> bool:
    return role_of(prof) in COACH_ROLES
