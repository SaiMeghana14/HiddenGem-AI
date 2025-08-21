from fastapi import APIRouter
from guides.translator import translate, phrasebook_lookup

router = APIRouter()

@router.get("/text")
def translate_text(text: str, src: str = "auto", dest: str = "hi"):
    return translate(text, dest, src)

@router.get("/phrasebook")
def phrasebook(text: str, dest: str, src: str="en"):
    translated = phrasebook_lookup(text, dest)
    return {"translated": translated or ""}
