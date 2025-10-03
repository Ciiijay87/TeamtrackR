import streamlit as st

PALETTE = {
    "present": "#4CAF50",   # grün
    "late": "#FF9800",      # orange
    "excused": "#2196F3",   # blau
    "absent": "#F44336",    # rot
}

def lang():
    return st.session_state.get("lang", "DE")

def t(de: str, en: str):
    return de if lang() == "DE" else en

def chip(text, bg="#eee"):
    st.markdown(f"<span style='background:{bg}; padding:4px 8px; border-radius:12px;'>{text}</span>", unsafe_allow_html=True)
