from fastapi import APIRouter
from app.services.analytics_service import get_data

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/get-data")

def data():
    return get_data()
