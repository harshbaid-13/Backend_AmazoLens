from app.dependencies.clickhouse import get_clickhouse_client
import pandas as pd
import datetime

def heatmap_data(until_days: int = 90):
    client = get_clickhouse_client()
    base_date = "2022-04-01"
    query = f"""
        SELECT 
            ul.state_ut, 
            SUM(s.quantity * s.unit_selling_price) AS total_sales
        FROM sales AS s
        JOIN users_location AS ul 
        ON s.customer_id = ul.customer_id
        WHERE s.date BETWEEN toDate('{base_date}') 
                         AND addDays(toDate('{base_date}'), {until_days})
        GROUP BY ul.state_ut
        ORDER BY total_sales DESC
    """
    result = client.query(query)
    return result.result_rows

def racing_bar_data():
    client = get_clickhouse_client()
    result = client.query("""
        SELECT 
            toStartOfWeek(s.date) AS week_start,
            p.product_name,
            SUM(s.quantity) AS total_quantity
        FROM sales s
        JOIN products p ON s.product_id = p.product_id
        WHERE s.date BETWEEN '2022-04-01' AND '2022-06-30'
        GROUP BY week_start, p.product_name
        ORDER BY week_start ASC, total_quantity DESC
        LIMIT 10 BY week_start
    """)
    return result.result_rows