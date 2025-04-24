# app/routes/forecasting_routes.py
from fastapi import APIRouter
from app.services.forecasting_service import (
    get_top_products,
    get_forecast_for_product,
)

router = APIRouter(prefix="/forecast", tags=["forecast"])

@router.get("/top-products")
def route_top_products():
    return get_top_products()

@router.get("/predict")
def route_forecast(product_id: int, granularity: str = "daily", days: int = 30):
    return get_forecast_for_product(product_id, granularity, days)
