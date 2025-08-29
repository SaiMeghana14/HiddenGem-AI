from fastapi import APIRouter

router = APIRouter()

@router.get("/translate")
def translate(text: str = "Hello", target_lang: str = "Hindi"):
    mock_translations = {
        "Hindi": "नमस्ते",
        "Telugu": "హలో",
        "French": "Bonjour"
    }
    translated = mock_translations.get(target_lang, text)
    return {"text": text, "target_lang": target_lang, "translation": translated}

@router.get("/phrasebook")
def phrasebook(text: str, src: str = "auto", dest: str = "en"):
    return {
        "original": text,
        "src": src,
        "dest": dest,
        "translation": f"[{dest}] {text}"
    }
