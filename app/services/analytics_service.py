from app.dependencies.clickhouse import get_clickhouse_client

def get_data():
    client = get_clickhouse_client()
    result = client.query("""
        SELECT * FROM sales
    """)
    return result.result_rows