from fastapi import APIRouter
from app.services.top_brands_service import top_brands

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/top-brands")

def data():
    return top_brands()
