from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import recommend, itinerary, transport, culture_food, safety, community, bookings

app = FastAPI(title="HiddenGem API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(recommend.router, prefix="/recommend", tags=["recommend"])
app.include_router(itinerary.router, prefix="/itinerary", tags=["itinerary"])
app.include_router(transport.router, prefix="/transport", tags=["transport"])
app.include_router(culture_food.router, prefix="/culture_food", tags=["culture_food"])
app.include_router(safety.router, prefix="/safety", tags=["safety"])
app.include_router(community.router, prefix="/community", tags=["community"])
app.include_router(bookings.router, prefix="/bookings", tags=["bookings"])

@app.get("/health")
def health():
    return {"status":"ok"}
