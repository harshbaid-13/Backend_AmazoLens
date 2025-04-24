from fastapi import APIRouter, Query
from fastapi.concurrency import run_in_threadpool
from app.services.dashboard_services import (
    heatmap_data,
    racing_bar_data,
    get_basic_data,
    get_pie_chart_data,
    get_weekly_sales_data
)
from typing import Optional

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/heatmap-data")
async def heatmap(until_days: int = Query(90)):
    return await run_in_threadpool(heatmap_data, until_days)

@router.get("/racing-bar")
async def racing_bar():
    return await run_in_threadpool(racing_bar_data)

@router.get("/get-data")
async def data(month: str = Query("2022-06-01", description="Month in YYYY-MM-DD format")):
    return await run_in_threadpool(get_basic_data, month)

@router.get("/pie-data")
async def pie_data(
    level: int = Query(..., description="Category level (1-3)"), 
    cat1: Optional[str] = Query(None, description="Category 1 value"), 
    cat2: Optional[str] = Query(None, description="Category 2 value"),
    others_only: bool = Query(False)
):
    if level < 1 or level > 3:
        return []

    if level >= 2 and not cat1:
        return []

    if level == 3 and not cat2:
        return []

    return await run_in_threadpool(
        get_pie_chart_data,
        level,
        l0_category=cat1,
        l1_category=cat2,
        others_only=others_only
    )

@router.get("/weekly-sales")
async def weekly_sales(
    start_date: Optional[str] = Query("2022-04-01", description="Start date in YYYY-MM-DD format"),
    end_date: Optional[str] = Query("2022-06-30", description="End date in YYYY-MM-DD format")
):
    return await run_in_threadpool(get_weekly_sales_data, start_date, end_date)
