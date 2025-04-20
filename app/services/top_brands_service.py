from app.dependencies.clickhouse import get_clickhouse_client
import json

def top_brands():
    client = get_clickhouse_client()
    result = client.query("""
        SELECT 
            p.brand_name,
            s.product_id,
            COUNT(*) AS product_count
        FROM 
            sales s
        INNER JOIN 
            products p 
        ON 
            s.product_id = p.product_id
        WHERE 
            p.brand_name IS NOT NULL
            AND s.product_id IS NOT NULL
        GROUP BY 
            p.brand_name, s.product_id
        HAVING 
            product_count > 0
        ORDER BY 
            product_count DESC
        LIMIT 100 

    """)

    columns = result.column_names  # e.g., ['brand_name', 'product_id', 'product_count']
    rows = result.result_rows      # List of tuples

    # Convert rows to list of dicts
    data = [dict(zip(columns, row)) for row in rows]

    # Convert to JSON string
    json_data = json.dumps(data)
    return json_data