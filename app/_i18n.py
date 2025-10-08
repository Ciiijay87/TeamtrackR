# _i18n.py
import streamlit as st

LANG_KEY = "lang"

def get_lang() -> str:
    # "DE" oder "EN" – Default: Deutsch
    return st.session_state.get(LANG_KEY, "DE").upper()

def set_lang(lang: str) -> None:
    st.session_state[LANG_KEY] = lang.upper()

def t(de: str, en: str) -> str:
    """Einfacher Übersetzer: gibt je nach Sprache DE/EN den passenden Text zurück."""
    return de if get_lang() == "DE" else en

def lang_selector():
    """Kleine Sprachwahl in der Seitenleiste."""
    lang = get_lang()
    sel = st.sidebar.selectbox(
        "Sprache / Language",
        options=["DE", "EN"],
        index=0 if lang == "DE" else 1,
    )
    if sel != lang:
        set_lang(sel)
        st.rerun()
