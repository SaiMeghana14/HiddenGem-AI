from typing import List
import re

MOOD_KEYWORDS = {
    "adventurous": ["adventure", "adventurous", "trek", "hike", "kayak", "climb", "thrill"],
    "calm": ["calm", "quiet", "peace", "relax", "spa", "park", "book"],
    "foodie": ["food", "eat", "biryani", "chai", "cafe", "restaurant", "street", "bakery"],
    "nightlife": ["night", "music", "club", "live", "bar"],
    "culture": ["heritage", "history", "museum", "craft", "temple", "class"],
}
INTENT_PATTERNS = {
    "plan_itinerary": r"(plan|itinerary|schedule|route)",
    "find_food": r"(food|eat|restaurant|cafe|chai|biryani|thali|bakery)",
    "find_stay": r"(stay|hotel|hostel|homestay)",
}

def detect_mood(text: str) -> str:
    t = text.lower()
    for mood, kws in MOOD_KEYWORDS.items():
        if any(k in t for k in kws):
            return mood
    return "neutral"

def detect_intents(text: str) -> List[str]:
    t = text.lower()
    found = []
    for name, pat in INTENT_PATTERNS.items():
        if re.search(pat, t):
            found.append(name)
    return found
