from fastapi import APIRouter
from app.services.quantity_items_service import quantity_items

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/quantity-items")

async def data():
    return await quantity_items()
