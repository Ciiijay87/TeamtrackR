# app/_i18n.py
def t(key: str, lang: str = "DE") -> str:
    de = {
        "home.title": "TeamtrackR",
        "home.subtitle.events": "📅 Termine / Events",
        "home.subtitle.attendance": "✅ Anwesenheit",
        "home.subtitle.tasks": "🧾 Aufgaben",
        "please_login": "Bitte einloggen.",
        "saved": "Gespeichert.",
        "error": "Fehler",
    }
    en = {
        "home.title": "TeamtrackR",
        "home.subtitle.events": "📅 Events / Calendar",
        "home.subtitle.attendance": "✅ Attendance",
        "home.subtitle.tasks": "🧾 Tasks",
        "please_login": "Please sign in.",
        "saved": "Saved.",
        "error": "Error",
    }
    base = de if (lang or "DE").upper().startswith("DE") else en
    return base.get(key, key)
