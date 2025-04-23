from fastapi import APIRouter

from app.services.topic_data_service import get_topic_data

router = APIRouter(prefix="/topic-sentiment", tags=["Topic"])


@router.get("/topics")
def get_topics():
    return get_topic_data()
