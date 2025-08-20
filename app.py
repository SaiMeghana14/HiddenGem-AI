import streamlit as st
import requests
import os
import json
import folium
from folium.plugins import MarkerCluster
from streamlit.components.v1 import html
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

BACKEND = st.session_state.get("backend_url", os.getenv("BACKEND_URL","http://localhost:8000"))

st.set_page_config(page_title="HiddenGem AI", layout="wide")
st.title("HiddenGem — Smart Travel Companion ✨")

with st.sidebar:
    st.header("Settings")
    backend_url = st.text_input("Backend URL", value=BACKEND)
    st.session_state["backend_url"] = backend_url
    city = st.selectbox("City", ["Hyderabad"])  # add more with data
    solo = st.checkbox("Solo Traveler Mode", value=False)
    sustain = st.checkbox("Sustainability Filter 🌱", value=False)
    budget = st.number_input("Budget per day (₹)", value=500, step=50)
    prefs = st.multiselect("Preferences", ["nature","food","history","nightlife","adventure","photo","calm","veg","eco","music","class"])

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "🔎 Discover", "🗺️ Plan", "🚖 Navigate", "🍴 Food & Culture",
    "🏨 Stay & Safety", "📸 AR & Diary", "🤝 Community", "🛒 Bookings"
])

def api_get(path, **params):
    try:
        r = requests.get(f"{backend_url}{path}", params=params, timeout=10)
        return r.json()
    except Exception as e:
        st.error(f"API error: {e}")
        return {}

def api_post(path, **params):
    try:
        r = requests.post(f"{backend_url}{path}", params=params, timeout=10, json=params if not params else None)
        return r.json()
    except Exception as e:
        st.error(f"API error: {e}")
        return {}

# 🔎 Discover
with tab1:
    st.subheader("Smart Discovery")
    mood_text = st.text_input("Tell me your vibe (e.g., 'I feel adventurous today')", "")
    mood = None
    intents = []
    if st.button("Detect Mood & Intent"):
        m = api_get("/recommend/mood", q=mood_text)
        mood = m.get("mood")
        intents = m.get("intents", [])
        st.info(f"Mood: **{mood}**, Intents: {', '.join(intents) or '-'}")
    resp = api_get("/recommend/hidden_gems", city=city, mood=mood, preferences=prefs, budget_per_day=budget, solo_mode=solo, sustainability=sustain)
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
        # Export PDF
        if st.button("Export Trip Diary (PDF)"):
            path = "trip_diary.pdf"
            c = canvas.Canvas(path, pagesize=A4)
            w, h = A4
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, h-50, f"HiddenGem Trip Diary — {city}")
            y = h-90
            for day in plan["plan"]:
                c.setFont("Helvetica-Bold", 14)
                c.drawString(50, y, f"Day {day['day']}")
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

# 🚖 Navigate
with tab3:
    st.subheader("Smart Route Mapping")
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
    stay = [{"name":"Hidden Boutique Homestay","price":1500},{"name":"Backpackers Hub Hostel","price":400}]
    for s in stay: st.write(f"- {s['name']} · ₹{s['price']}")
    alerts = api_get("/safety/alerts", city=city).get("alerts", [])
    if alerts:
        st.warning("Safety Alerts:")
        for a in alerts: st.write(f"- {a['type'].title()}: {a['msg']}")

# 📸 AR & Diary
with tab6:
    st.subheader("Photo Spot Detector & AR Facts (MVP)")
    st.caption("Hint: Pick photogenic places, then click 'Generate Fun Facts'")
    photo_spots = [it for it in items if it.get("photogenic")] if items else []
    for p in photo_spots:
        st.write(f"📸 {p['name']} — great for photos")
    if st.button("Generate Fun Facts"):
        for p in photo_spots[:5]:
            st.info(f"**{p['name']}** — Built with local heritage influence. Great at golden hour. (Demo fact)")

# 🤝 Community
with tab7:
    st.subheader("Community Hidden Gems")
    name = st.text_input("Place name")
    lat = st.number_input("Lat", value=17.3850)
    lon = st.number_input("Lon", value=78.4867)
    cat = st.selectbox("Category", ["food","culture","adventure","nature","photo","stay","nightlife"])
    tags = st.text_input("Tags (comma-separated)", value="local,authentic")
    notes = st.text_area("Notes")
    if st.button("Submit Place"):
        r = api_post("/community/submit", name=name, city=city, lat=float(lat), lon=float(lon), category=cat, tags=tags, notes=notes)
        st.success(f"Submitted! id={r.get('id')}")
    st.write("Top Community Spots")
    r = api_get("/community/list", city=city)
    for it in r.get("items", []):
        st.write(f"- {it['name']} · votes: {it['votes']}")
        st.button(f"👍 Upvote {it['id']}", key=f"up{it['id']}", on_click=lambda pid=it['id']: api_post("/community/vote", place_id=pid, up=True))

# 🛒 Bookings
with tab8:
    st.subheader("Smart Bookings & Deals (Stubs)")
    st.caption("Plug your favorite providers' APIs here (e.g., RapidAPI, Amadeus, IRCTC partner, etc.)")
    b = api_get("/bookings/search_stay", city=city, budget=int(budget))
    for r in b.get("results", []):
        st.write(f"- {r['name']} · ₹{r['price']}")
    e = api_get("/bookings/search_events", city=city)
    st.write("Events:")
    for r in e.get("results", []):
        st.write(f"- {r['title']} · {r['when']} · ₹{r['price']}")
