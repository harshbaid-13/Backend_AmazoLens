from fastapi import APIRouter, Query
from app.services.dashboard_services import (
    heatmap_data,
    racing_bar_data,
)

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/heatmap-data")
def heatmap(until_days: int = Query(90)):
    return heatmap_data(until_days)

@router.get("/racing-bar")
def racing_bar():
    return racing_bar_data()

# @router.get("/total-sales")
# def total_sales():
#     return { "total_sales": get_total_sales() }

# @router.get("/total-orders")
# def total_orders():
#     return { "total_orders": get_total_orders() }

# @router.get("/total-customers")
# def total_customers():
#     return { "total_customers": get_total_customers() }

# @router.get("/avg-order-value")
# def avg_order_value():
#     return { "avg_order_value": get_avg_order_value() }