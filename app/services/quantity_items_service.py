from app.dependencies.clickhouse import get_clickhouse_client
import json

async def quantity_items():
    client = await get_clickhouse_client()
    result = await client.query("""
        SELECT 
            sales.product_id,
            SUM(sales.quantity) AS total_quantity,
            products.product_name
        FROM 
            sales
        INNER JOIN 
            products
        ON 
            sales.product_id = products.product_id
        GROUP BY 
            sales.product_id, 
            products.product_name
        ORDER BY 
            total_quantity DESC
        LIMIT 100



    """)

    columns = result.column_names  
    rows = result.result_rows     

    # Convert rows to list of dicts
    data = [dict(zip(columns, row)) for row in rows]

    # Convert to JSON string
    json_data = json.dumps(data)
    return json_data