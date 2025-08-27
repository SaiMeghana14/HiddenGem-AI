import streamlit as st
import requests
import os
import json
import folium
from folium.plugins import MarkerCluster
from streamlit.components.v1 import html
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

st.set_page_config(page_title="HiddenGem AI", layout="wide")
st.title("HiddenGem — Smart Travel Companion ✨")

# Backend URL
BACKEND = st.session_state.get("backend_url", os.getenv("BACKEND_URL","https://hiddengem-ai.onrender.com"))

def api_get(path, **params):
    try:
        r = requests.get(f"{BACKEND}{path}", params=params, timeout=12)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"API error: {e}")
        return {}

def api_post(path, payload=None, **params):
    try:
        r = requests.post(f"{BACKEND}{path}", params=params, json=payload, timeout=12)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"API error: {e}")
        return {}

# Dynamic cities
city_resp = api_get("/meta/cities")
cities = city_resp.get("cities", ["Hyderabad"])

with st.sidebar:
    st.header("Settings")
    backend_url = st.text_input("Backend URL", value=BACKEND)
    st.session_state["backend_url"] = backend_url
    city = st.selectbox("City", cities)
    solo = st.checkbox("Solo Traveler Mode", value=False)
    sustain = st.checkbox("Sustainability Filter 🌱", value=False)
    family = st.checkbox("Family-Friendly Filter 👨‍👩‍👧‍👦", value=False)
    accessible = st.checkbox("Wheelchair Accessible ♿", value=False)
    budget = st.number_input("Budget per day (₹)", value=500, step=50)
    prefs = st.multiselect("Preferences", ["nature","food","history","nightlife","adventure","photo","calm","veg","eco","music","class"])

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
    "🔎 Discover", "🗺️ Plan", "🚖 Navigate", "🍴 Food & Culture",
    "🏨 Stay & Safety", "📸 AR & Facts", "📓 Travel Diary", "🤝 Community", "🛒 Bookings", "🗣️ Translator"
])

# 🔎 Discover
with tab1:
    st.subheader("Smart Discovery")
    mood_text = st.text_input("Tell me your vibe (e.g., 'I feel adventurous today')", "")
    mood, intents = None, []
    if st.button("Detect Mood & Intent"):
        m = api_get("/recommend/mood", q=mood_text)
        mood = m.get("mood")
        intents = m.get("intents", [])
        st.info(f"Mood: **{mood}**, Intents: {', '.join(intents) or '-'}")
    resp = api_get(
        "/recommend/hidden_gems",
        city=city,
        mood=mood,
        preferences=prefs,
        budget_per_day=budget,
        solo_mode=solo,
        sustainability=sustain,
        family=family,
        accessible=accessible
    )
    items = resp.get("items", [])
    c1, c2 = st.columns([1,1])
    with c1:
        st.write(f"**Top {len(items)} Hidden Gems**")
        for it in items:
            st.markdown(f"- **{it['name']}** · {it['category']} · ₹{it['cost']} · ⭐ {it['rating']} · Safety {it['safety']} {'· 🌱' if it['sustainability'] else ''}")
    with c2:
        if items:
            m = folium.Map(location=[items[0]["lat"], items[0]["lon"]], zoom_start=12)
            mc = MarkerCluster().add_to(m)
            for it in items:
                folium.Marker([it["lat"], it["lon"]], tooltip=it["name"], popup=f"{it['name']} ({it['category']})").add_to(mc)
            html(m._repr_html_(), height=450)

# 🗺️ Plan
with tab2:
    st.subheader("AI Itinerary Planner")
    days = st.slider("Days", 1, 7, 2)
    if st.button("Generate Itinerary"):
        plan = api_post("/itinerary/plan", city=city, days=days, budget_per_day=int(budget), preferences=prefs)
        st.session_state["plan"] = plan
    plan = st.session_state.get("plan")
    if plan:
        total = 0
        for day in plan["plan"]:
            st.markdown(f"**Day {day['day']}** — est. budget ₹{day['est_budget']}")
            total += day['est_budget']
            for s in day["stops"]:
                st.write(f"- {s['name']} · {s['category']} · ₹{s['cost']}")
        st.info(f"Trip total ~ ₹{total}")
        guide = api_get("/meta/guide", city=city).get("guide")
        if guide: st.success(f"📖 City Guide: {guide}")

# 🚖 Navigate
with tab3:
    st.subheader("Smart Route Mapping")
    resp = api_get("/recommend/hidden_gems", city=city, budget_per_day=budget)
    items = resp.get("items", [])
    if items:
        start = items[0]; end = items[-1]
        r = api_get("/transport/route", start_lat=start["lat"], start_lon=start["lon"], end_lat=end["lat"], end_lon=end["lon"], mode="walk")
        st.write(r)
        m = folium.Map(location=[start["lat"], start["lon"]], zoom_start=12)
        folium.PolyLine([(start["lat"], start["lon"]), (end["lat"], end["lon"])]).add_to(m)
        folium.Marker([start["lat"], start["lon"]], tooltip="Start").add_to(m)
        folium.Marker([end["lat"], end["lon"]], tooltip="End").add_to(m)
        html(m._repr_html_(), height=420)

# 🍴 Food & Culture
with tab4:
    st.subheader("Hidden Food Spots & Cultural Experiences")
    f = api_get("/culture_food/food_spots", city=city, authentic=True)
    c = api_get("/culture_food/cultural", city=city)
    st.write("**Food**")
    for x in f.get("items", []): st.write(f"- {x['name']} · ₹{x['cost']} · ⭐ {x['rating']}")
    st.write("**Culture**")
    for x in c.get("items", []): st.write(f"- {x['name']} · {x['category']}")

# 🏨 Stay & Safety
with tab5:
    st.subheader("Stay Suggestions & Safety Alerts")
    stay = api_get("/stay/search", city=city, budget=int(budget)).get("stays", [])
    if not stay:
        stay = [{"name":"Hidden Boutique Homestay","price":1500},{"name":"Backpackers Hub Hostel","price":400}]
    for s in stay: st.write(f"- {s['name']} · ₹{s['price']}")
    alerts = api_get("/safety/alerts", city=city).get("alerts", [])
    if alerts:
        st.warning("Safety Alerts:")
        for a in alerts: st.write(f"- {a['type'].title()}: {a['msg']}")

# 📸 AR & Facts
with tab6:
    st.subheader("AR & Facts")
    resp = api_get("/recommend/hidden_gems", city=city, budget_per_day=budget)
    items = resp.get("items", [])
    photogenic = [it for it in items if it.get("photogenic")] if items else []
    if photogenic:
        name = st.selectbox("Pick a place for a quick fact:", [p["name"] for p in photogenic])
        if st.button("Get Landmark Fact"):
            fact = api_get("/facts/summary", query=name).get("fact", "No fact.")
            st.info(f"📖 **{name}** — {fact}")
        if st.button("Use Vision API (Demo)"):
            vision = api_get("/facts/vision", query=name).get("vision_fact", "Vision API not connected.")
            st.success(f"👓 Vision Insight: {vision}")
    else:
        st.caption("No photogenic spots in current filter.")

# 📓 Travel Diary
with tab7:
    st.subheader("Travel Diary Export")
    plan = st.session_state.get("plan")
    if not plan:
        st.info("Generate an itinerary first in the Plan tab.")
    else:
        if st.button("Export Trip Diary (PDF)"):
            path = "trip_diary.pdf"
            c = canvas.Canvas(path, pagesize=A4)
            w, h = A4
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, h-50, f"HiddenGem Trip Diary — {plan.get('city')}")
            y = h-90
            for day in plan["plan"]:
                c.setFont("Helvetica-Bold", 14)
                c.drawString(50, y, f"Day {day['day']} (₹{day['est_budget']})")
                y -= 20
                c.setFont("Helvetica", 12)
                for s in day["stops"]:
                    c.drawString(60, y, f"- {s['name']} ({s['category']})")
                    y -= 18
                    if y < 80:
                        c.showPage()
                        y = h-80
            c.showPage(); c.save()
            with open(path, "rb") as f:
                st.download_button("Download PDF", data=f, file_name="HiddenGem_TripDiary.pdf")

# 🤝 Community + Gamification
with tab8:
    st.subheader("Community Hidden Gems & Badges")
    name = st.text_input("Place name")
    lat = st.number_input("Lat", value=17.3850)
    lon = st.number_input("Lon", value=78.4867)
    cat = st.selectbox("Category", ["food","culture","adventure","nature","photo","stay","nightlife"])
    tags = st.text_input("Tags (comma-separated)", value="local,authentic")
    notes = st.text_area("Notes")
    if st.button("Submit Place"):
        r = api_post("/community/submit", dict(), name=name, city=city, lat=float(lat), lon=float(lon), category=cat, tags=tags, notes=notes)
        st.success(f"Submitted! id={r.get('id')}")
    st.write("Top Community Spots")
    r = api_get("/community/list", city=city)
    for it in r.get("items", []):
        col1, col2, col3 = st.columns([3,1,1])
        with col1:
            st.write(f"- {it['name']} · votes: {it['votes']} · visits: {it.get('visits',0)}")
        with col2:
            st.button(f"👍 {it['id']}", key=f"up{it['id']}", on_click=lambda pid=it['id']: api_post("/community/vote", dict(), place_id=pid, up=True))
        with col3:
            st.button(f"✅ Visit", key=f"visit{it['id']}", on_click=lambda pid=it['id']: api_post("/community/visit", dict(), place_id=pid))
    # Badge status
    badges = api_get("/community/badges", user="me").get("badges", [])
    if badges: st.success(f"🏅 Your Badges: {', '.join(badges)}")
    else: st.caption("No badges earned yet. Visit, upvote, and submit to earn HiddenGem Badges!")

# 🛒 Bookings
with tab9:
    st.subheader("Smart Bookings & Deals (Stubs)")
    b = api_get("/bookings/search_stay", city=city, budget=int(budget))
    for r in b.get("results", []):
        st.write(f"- {r['name']} · ₹{r['price']}")
    e = api_get("/bookings/search_events", city=city)
    st.write("Events:")
    for r in e.get("results", []):
        st.write(f"- {r['title']} · {r['when']} · ₹{r['price']}")

# 🗣️ Translator
with tab10:
    st.subheader("AI Translator (with phrasebook fallback)")
    text = st.text_input("Enter text")
    src = st.selectbox("Source", ["auto","en","hi","te","es","fr","de"], index=0)
    dest = st.selectbox("Target", ["hi","en","te","es","fr","de"], index=0)
    if st.button("Translate"):
        res = api_get("/translate/text", text=text, src=src, dest=dest)
        if res.get("translated"):
            st.write(f"**Translated** ({res.get('source')}): {res.get('translated')}")
        else:
            st.warning("Translation API not available. Falling back to phrasebook.")
            phrase = api_get("/translate/phrasebook", text=text, src=src, dest=dest).get("translated", "No phrase found.")
            st.info(f"📖 Phrasebook: {phrase}")
