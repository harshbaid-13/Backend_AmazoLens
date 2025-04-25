from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from typing import Optional
from datetime import date

from app.services.analytics_service import (
    get_data,
    get_folium,
    get_top_cities,
    get_top_products_by_state_month,
    get_sales_by_state_ut,
    get_sales_by_month_for_state,
    get_top_products_by_state_month
)

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/get-data")
def data():
    return get_data()

@router.get("/get-folium")
def data(
    from_date: Optional[date] = Query('2022-04-02'),
    to_date: Optional[date] = Query('2022-04-02')
):
    map_str = get_folium(str(from_date), str(to_date))
    return JSONResponse(content={"map_html": map_str})

@router.get("/get-top-cities")
def data(
    from_date: Optional[date] = Query('2022-04-02'),
    to_date: Optional[date] = Query('2022-04-02')
):
    cities = get_top_cities(str(from_date), str(to_date))
    return cities

# @router.get("/top-product-state-month")
# def top_products_by_state_month(
#     from_date: Optional[date] = Query('2022-04-01'),
#     to_date: Optional[date] = Query('2022-06-30')
# ):
#     data = get_top_products_by_state_month(str(from_date), str(to_date))
#     return data


@router.get("/get-sales-by-state")
def get_sales_by_state(
    from_date: Optional[str] = Query('2022-04-01'),
    to_date: Optional[str] = Query('2022-06-30')
):
    data = get_sales_by_state_ut(from_date, to_date)
    return JSONResponse(content={"data": data})

# Get sales data for each month for a selected state/UT (Second Level Drill-Down)
@router.get("/get-sales-by-month")
def get_sales_by_month(
    state_ut: str = Query(...),
    from_date: Optional[str] = Query('2022-04-01'),
    to_date: Optional[str] = Query('2022-06-30')
):
    data = get_sales_by_month_for_state(state_ut, from_date, to_date)
    return JSONResponse(content={"data": data})

# Get top 5 products for a specific state/UT and month (Third Level Drill-Down)
@router.get("/get-top-products")
def get_top_products(
    state_ut: str = Query(...),
    month: int = Query(...),
    from_date: Optional[str] = Query('2022-04-01'),
    to_date: Optional[str] = Query('2022-06-30')
):
    data = get_top_products_by_state_month(state_ut, month, from_date, to_date)
    return JSONResponse(content={"data": data})