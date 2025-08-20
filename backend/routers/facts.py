from fastapi import APIRouter
from ..services import facts as svc

router = APIRouter()

@router.get("/summary")
def summary(query: str):
    return {"query": query, "fact": svc.wikipedia_summary(query)}
