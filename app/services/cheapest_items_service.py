from app.dependencies.clickhouse import get_clickhouse_client_async
import json

async def cheapest_items():
    client = await get_clickhouse_client_async()
    result = await client.query("""
        SELECT 
            s.product_id,
            MIN(s.unit_selling_price) AS lowest_unit_selling_price,
            p.product_name,
            COUNT(*) AS sales_count
        FROM 
            sales s
        INNER JOIN 
            products p
        ON 
            s.product_id = p.product_id
        WHERE
            s.unit_selling_price >= 8
        GROUP BY 
            s.product_id, 
            p.product_name
        ORDER BY 
            lowest_unit_selling_price ASC
        LIMIT 500






    """)

    columns = result.column_names  
    rows = result.result_rows     

    # Convert rows to list of dicts
    data = [dict(zip(columns, row)) for row in rows]

    # Convert to JSON string
    json_data = json.dumps(data)
    return json_data