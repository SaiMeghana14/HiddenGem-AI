from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter

from .routers import (
    recommend, itinerary, transport, culture_food, stay,
    safety, community, bookings, translator, facts, meta
)

app = FastAPI(title="HiddenGem API", version="0.2.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

# ------------------ Include Routers ------------------
app.include_router(recommend.router, prefix="/recommend", tags=["recommend"])
app.include_router(itinerary.router, prefix="/itinerary", tags=["itinerary"])
app.include_router(transport.router, prefix="/transport", tags=["transport"])
app.include_router(culture_food.router, prefix="/culture_food", tags=["culture_food"])
app.include_router(safety.router, prefix="/safety", tags=["safety"])
app.include_router(community.router, prefix="/community", tags=["community"])
app.include_router(bookings.router, prefix="/bookings", tags=["bookings"])

# New features
app.include_router(translator.router, prefix="/translate", tags=["translate"])
app.include_router(facts.router, prefix="/facts", tags=["facts"])
app.include_router(meta.router, prefix="/meta", tags=["meta"])
app.include_router(stay.router, prefix="/stay", tags=["stay"])


# ------------------ Health Check ------------------
@app.get("/health")
def health():
    return {"status": "ok"}


# ------------------ Meta Cities ------------------
@app.get("/meta/cities")
def list_cities():
    return {
        "cities": [
            "Hyderabad", 
            "Bengaluru", 
            "Mumbai", 
            "Delhi", 
            "Chennai", 
            "Kolkata", 
            "Pune", 
            "Jaipur", 
            "Goa"
        ]
    }


# ------------------ Root ------------------
@app.get("/")
def root():
    return {
        "message": "🚀 HiddenGem API is running!",
        "endpoints": {
            "health": "/health",
            "cities": "/meta/cities",
            "docs": "/docs"
        }
    }


# ------------------ Ensure Required Subroutes ------------------
# If your routers don’t already define these, add fallbacks here
# This prevents 404 errors until you implement real logic

router = APIRouter()

@router.get("/recommend/mood")
def recommend_by_mood(q: str = "adventurous"):
    return {"mood": q, "recommendations": ["Sample Place 1", "Sample Place 2"]}

@router.get("/itinerary/plan")
def itinerary_plan(city: str = "Hyderabad", days: int = 2, budget_per_day: int = 500):
    return {
        "city": city,
        "days": days,
        "budget_per_day": budget_per_day,
        "itinerary": [
            {"day": 1, "activities": ["Visit landmark A", "Eat at local spot"]},
            {"day": 2, "activities": ["Explore park B", "Try cultural show"]}
        ]
    }

@router.get("/translate/text")
def translate_text(text: str, src: str = "auto", dest: str = "hi"):
    return {"input": text, "src": src, "dest": dest, "output": f"[{text}] translated to {dest}"}


# Attach fallback router
app.include_router(router)
