from clickhouse_connect import get_client
from app.config import settings

client = get_client(
    host=settings.CLICKHOUSE_HOST,
    username=settings.CLICKHOUSE_USER,
    password=settings.CLICKHOUSE_PASSWORD,
    secure=True
)

def get_clickhouse_client():
    return client
