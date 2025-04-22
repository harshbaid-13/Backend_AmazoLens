from fastapi import APIRouter
from app.services.cheapest_items_service import cheapest_items

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/cheapest-items")

async def data():
    return await cheapest_items()
