from app.dependencies.clickhouse import get_clickhouse_client
import json

async def cheapest_items():
    client = await get_clickhouse_client()
    result = await client.query("""
        SELECT 
            sales.product_id,
            MIN(sales.unit_selling_price) AS lowest_unit_selling_price,
            products.product_name
        FROM 
            sales
        INNER JOIN 
            products
        ON 
            sales.product_id = products.product_id
        WHERE
            sales.unit_selling_price >= 8
        GROUP BY 
            sales.product_id, 
            products.product_name
        ORDER BY 
            lowest_unit_selling_price ASC
        LIMIT 200






    """)

    columns = result.column_names  
    rows = result.result_rows     

    # Convert rows to list of dicts
    data = [dict(zip(columns, row)) for row in rows]

    # Convert to JSON string
    json_data = json.dumps(data)
    return json_data