from clickhouse_connect import get_async_client
from clickhouse_connect.driver.httputil import get_pool_manager
from app.config import settings

# Initialize a connection pool for async (shared across clients)
pool_mgr = get_pool_manager(num_pools=10)  # Adjust based on expected concurrency

async def get_clickhouse_client():
    """Create a new AsyncClient instance for each coroutine/task"""
    client = await get_async_client(
        host=settings.CLICKHOUSE_HOST,
        username=settings.CLICKHOUSE_USER,
        password=settings.CLICKHOUSE_PASSWORD,
        secure=True,
        pool_mgr=pool_mgr  # Reuse the connection pool
    )
    return client
