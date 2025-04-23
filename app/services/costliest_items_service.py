from app.dependencies.clickhouse import get_clickhouse_client_async
import json

async def costliest_items():
    client = await get_clickhouse_client_async()
    result = await client.query("""
        SELECT 
            sales.product_id,
            MAX(sales.unit_selling_price) AS highest_unit_selling_price,
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
            highest_unit_selling_price DESC
        LIMIT 100




    """)

    columns = result.column_names  
    rows = result.result_rows     

    # Convert rows to list of dicts
    data = [dict(zip(columns, row)) for row in rows]

    # Convert to JSON string
    json_data = json.dumps(data)
    return json_data