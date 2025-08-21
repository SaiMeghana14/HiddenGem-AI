from fastapi import APIRouter

router = APIRouter()

@router.get("/facts")
def get_facts(city: str = "Hyderabad"):
    facts = [
        f"{city} is known as the City of Pearls.",
        f"{city} houses the famous Charminar.",
        f"{city} is a hub for IT and film industry."
    ]
    return {"city": city, "results": facts}
