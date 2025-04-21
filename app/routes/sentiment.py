from fastapi import APIRouter
from app.services.sentiment_service import (
    get_categories,
    get_overall_sentiment,
    get_sentiment_trend,
    get_sentiment_by_category,
    get_recent_reviews
)

router = APIRouter(prefix="/sentiment", tags=["sentiment"])

@router.get("/get-categories")
def route_get_categories():
    return get_categories()

@router.get("/overall")
def route_overall():
    return get_overall_sentiment()

@router.get("/trend")
def route_trend():
    return get_sentiment_trend()

@router.get("/by-category")
def route_category_sentiment():
    return get_sentiment_by_category()

@router.get("/reviews")
def route_recent_reviews(limit: int = 5):
    return get_recent_reviews(limit)
