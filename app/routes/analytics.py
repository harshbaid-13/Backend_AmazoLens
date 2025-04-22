from fastapi import APIRouter,Query
from fastapi.responses import JSONResponse
from app.services.analytics_service import get_data,get_folium,get_top_cities
from typing import Optional
from datetime import date

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/get-data")

def data():
    return get_data()

@router.get("/get-folium")
def data(
    from_date: Optional[date] = Query('2022-04-02'),
    to_date: Optional[date] = Query('2022-04-02')
):
    # print(type(from_date))
    # print(type(str(from_date)))
    map_str=get_folium(str(from_date), str(to_date))
    return  JSONResponse(content={"map_html": map_str})

@router.get("/get-top-cities")
def data(
    from_date: Optional[date] = Query('2022-04-02'),
    to_date: Optional[date] = Query('2022-04-02')
):
    cities = get_top_cities(str(from_date), str(to_date))
    return cities
