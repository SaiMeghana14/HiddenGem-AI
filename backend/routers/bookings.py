from fastapi import APIRouter
router = APIRouter()

@router.get("/search_stay")
def search_stay(city: str = "Hyderabad", budget: int = 1500):
    return {"city": city, "results": [
        {"name":"Hidden Boutique Homestay", "price": budget, "url":"#"},
        {"name":"Backpackers Hub Hostel", "price": max(300, budget//3), "url":"#"}
    ]}

@router.get("/search_events")
def search_events(city: str = "Hyderabad"):
    return {"city": city, "results": [
        {"title":"Handicraft Workshop", "when":"Sat 11am", "price": 300},
        {"title":"Indie Live Music", "when":"Fri 8pm", "price": 500},
    ]}
