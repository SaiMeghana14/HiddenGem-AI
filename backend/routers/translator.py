from fastapi import APIRouter, Query
from data import phrasebook

router = APIRouter(prefix="/translator", tags=["translator"])

@router.get("/translate")
def translate(phrase: str = Query(...), lang: str = Query("hindi")):
    translations = phrasebook.get_phrasebook()
    for p in translations:
        if p["english"].lower() == phrase.lower():
            return { "english": phrase, lang: p.get(lang, "Not available") }
    return {"message": "Phrase not found"}
