import os
from fastapi import APIRouter
from app.services.market_basket_service import get_category
from app.services.market_basket_service import get_frequent_itemsets_service
from app.services.market_basket_service import get_product_association_rules_service
from app.services.market_basket_service import get_heatmap_service
from app.services.market_basket_service import get_sankey_service
from app.services.market_basket_service import get_fp_service
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware



BASE_PATH = 'public/market_basket'
router = APIRouter(prefix="/market-basket", tags=["market-basket"])

@router.get("/get-category")
def data():
    return get_category()
@router.get("/frequent-itemsets")
def get_frequent_itemsets(category: str = Query(..., description="Category name as listed in get-category")):
    return get_frequent_itemsets_service(category)

@router.get("/get-product-association-rules")
def get_product_association_rules(category: str = Query(..., description="Category name as listed in get-category")):
    return get_product_association_rules_service(category)

@router.get("/get-heatmap")
def get_product_association_rules(category: str = Query(..., description="Category name as listed in get-category")):
    return get_heatmap_service(category)

@router.get("/get-sankey-Data")
def get_sankey(category: str = Query(..., description="Category name as listed in get-category")):
    return get_sankey_service(category)

@router.get("/get-fp-Data")
def get_fp(category: str = Query(..., description="Category name as listed in get-category")):
    return get_fp_service(category)