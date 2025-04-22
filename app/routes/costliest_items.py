from fastapi import APIRouter
from app.services.costliest_items_service import costliest_items

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/costliest-items")

async def data():
    return await costliest_items()
