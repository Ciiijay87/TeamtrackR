import streamlit as st
from _auth import require_login, is_staff, supa
from _data import list_categories

prof = require_login()
st.title("Termine / Events")

cats = list_categories()
cat_names = [c["name"] for c in cats]
tab_list, tab_new, tab_cat = st.tabs(["Übersicht", "Neu", "Kategorien"])

with tab_list:
    res = supa().table("events").select("*, event_categories(name)").order("starts_at").execute()
    events = res.data
    for e in events:
        vis = "Team" if e["visibility"]=="team" else "Staff"
        st.write(f"**{e['title']}** — {e['starts_at']} → {e['ends_at']} @ {e.get('location','')}")
        st.caption(f"{vis} • {e.get('description','')}")
        if is_staff(prof):
            if st.button(f"Delete #{e['id']}", key=f"del{e['id']}"):
                supa().table("events").delete().eq("id", e["id"]).execute()
                st.experimental_rerun()

with tab_new:
    if not is_staff(prof):
        st.info("Nur Staff/Coaches können Termine erstellen.")
    else:
        title = st.text_input("Titel")
        desc = st.text_area("Beschreibung")
        col1, col2 = st.columns(2)
        starts = col1.text_input("Start (YYYY-MM-DD HH:MM)")
        ends = col2.text_input("Ende (YYYY-MM-DD HH:MM)")
        loc = st.text_input("Ort")
        visibility = st.selectbox("Sichtbarkeit", ["team","staff"])
        cat = st.selectbox("Kategorie", cat_names) if cat_names else st.text_input("Kategorie (neu)")
        reminders = st.multiselect("Erinnerungen", ["48h","24h","2h","1h"], ["24h"])
        if st.button("Speichern"):
            cat_id = None
            if cat and cat not in cat_names:
                cat_row = supa().table("event_categories").insert({"name": cat}).execute().data[0]
                cat_id = cat_row["id"]
            else:
                for c in cats:
                    if c["name"] == cat:
                        cat_id = c["id"]
            supa().table("events").insert({
                "title": title, "description": desc,
                "starts_at": starts, "ends_at": ends,
                "location": loc, "visibility": visibility,
                "category_id": cat_id, "reminders": reminders, "created_by": prof["id"]
            }).execute()
            st.success("Termin gespeichert.")
            st.experimental_rerun()

with tab_cat:
    if is_staff(prof):
        newc = st.text_input("Neue Kategorie")
        if st.button("Anlegen") and newc:
            supa().table("event_categories").insert({"name": newc}).execute()
            st.experimental_rerun()
