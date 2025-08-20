from fastapi import APIRouter
from typing import Optional
from ..services import translator as svc

router = APIRouter()

@router.get("/text")
def translate_text(text: str, src: Optional[str] = "auto", dest: str = "hi"):
    out, source = svc.translate(text, src or "auto", dest)
    return {"text": text, "translated": out, "source": source}
