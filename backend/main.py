from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import (
    recommend, itinerary, transport, culture_food,
    safety, community, bookings, translator, facts, meta
)

app = FastAPI(title="HiddenGem API", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

# Existing features
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

@app.get("/health")
def health():
    return {"status": "ok"}

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
