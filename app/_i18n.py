import streamlit as st

LANG_KEY = "lang"

def get_lang() -> str:
    return st.session_state.get(LANG_KEY, "DE").upper()

def set_lang(lang: str) -> None:
    st.session_state[LANG_KEY] = lang.upper()

def t(de: str, en: str) -> str:
    """Mini-Übersetzer."""
    return de if get_lang() == "DE" else en

def lang_selector():
    """Sprachauswahl in der Sidebar + sofortiges Neu-Laden bei Wechsel."""
    sel = st.sidebar.selectbox(
        "Sprache / Language",
        options=["DE", "EN"],
        index=0 if get_lang() == "DE" else 1,
    )
    if sel != get_lang():
        set_lang(sel)
        st.rerun()
