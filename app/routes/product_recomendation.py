import os
from fastapi import APIRouter
from app.services.prod_recom_service import get_category
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from urllib.parse import unquote


BASE_PATH = 'public/prod_recom'
router = APIRouter(prefix="/prod-recom", tags=["prod-recom"])

@router.get("/get-category")
def data():
    return get_category()

@router.get("/prod-recom/get-data")
def get_data(category: str = Query(..., description="Category name as listed in get-category")):
    category = unquote(category)

    similarity_file = os.path.join(BASE_PATH, f"item_similarity_df_{category}.parquet")
    affinity_file = os.path.join(BASE_PATH, "prod_affinity_data", f"affinity_links_{category}.parquet")

    if not os.path.exists(similarity_file):
        raise HTTPException(status_code=404, detail=f"Similarity file for '{category}' not found.")
    if not os.path.exists(affinity_file):
        raise HTTPException(status_code=404, detail=f"Affinity file for '{category}' not found.")

    try:
        similarity_df = pd.read_parquet(similarity_file).reset_index()
        affinity_df = pd.read_csv(affinity_file).reset_index()

        return {
            "similarity_data": similarity_df.to_dict(orient="records"),
            "affinity_data": affinity_df.to_dict(orient="records")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading parquet files: {e}")
