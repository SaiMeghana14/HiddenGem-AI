from fastapi import APIRouter

router = APIRouter()

@router.get("/search")
def search_stays(city: str, budget: int):
    return {
        "city": city,
        "budget": budget,
        "results": [
            {"name": "Cozy Homestay", "price": budget - 100, "rating": 4.5},
            {"name": "Eco Hostel", "price": budget, "rating": 4.2}
        ]
    }
