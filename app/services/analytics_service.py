from app.dependencies.clickhouse import get_clickhouse_client
import pandas as pd
from app.aryan_files.functions import make_folium_map

def get_data():
    client = get_clickhouse_client()
    result = client.query("""
        SELECT * FROM sales
        LIMIT 1000
    """)
    return result.result_rows

def get_folium(from_date='2022-04-02', to_date='2022-04-02'):
    client = get_clickhouse_client()
    q_string = f"""
        SELECT * 
        FROM sales s 
        INNER JOIN users_location ul ON s.customer_id = ul.customer_id
        WHERE s.date >= '{str(from_date)}' AND s.date <= '{str(to_date)}'
    """
    result = client.query(q_string)
    sales = pd.DataFrame([row for row in result.result_rows])
    sales.columns = result.column_names
    return make_folium_map(sales)

def get_top_cities(from_date="", to_date=""):
    client = get_clickhouse_client()
    q_string = f"""
        SELECT 
            ul.state_ut, 
            ROUND(SUM(
                CASE 
                    WHEN CAST(s.total_weighted_landing_price AS String) ILIKE '%nan%' THEN 0
                    ELSE s.total_weighted_landing_price 
                END
            ),2) AS total_price
        FROM (
            SELECT 
                customer_id, 
                total_weighted_landing_price, 
                date 
            FROM sales 
            WHERE date BETWEEN '{str(from_date)}' AND '{str(to_date)}'
        ) s 
        INNER JOIN users_location ul ON s.customer_id = ul.customer_id 
        GROUP BY ul.state_ut 
        ORDER BY total_price DESC 
        LIMIT 10
    """
    result = client.query(q_string)
    return [{"state_ut": row[0], "total_price": row[1]} for row in result.result_rows]

def get_sales_by_state_ut(from_date='2022-04-02', to_date='2022-06-30'):
    client = get_clickhouse_client()
    query = f"""
        SELECT 
            ul.state_ut, 
            ROUND(SUM(CASE 
                WHEN CAST(s.total_weighted_landing_price AS String) ILIKE '%nan%' THEN 0
                ELSE s.total_weighted_landing_price 
            END), 2) AS total_sales
        FROM sales s
        INNER JOIN users_location ul ON s.customer_id = ul.customer_id
        WHERE s.date BETWEEN '{from_date}' AND '{to_date}'
        GROUP BY ul.state_ut
        ORDER BY total_sales DESC
    """
    result = client.query(query)
    return [{"state_ut": row[0], "total_sales": row[1]} for row in result.result_rows]

# Get monthly sales by state/UT for the given date range (drilldown to 3 months)
def get_sales_by_month_for_state(state_ut, from_date='2022-04-01', to_date='2022-06-30'):
    client = get_clickhouse_client()
    query = f"""
        SELECT 
            EXTRACT(MONTH FROM s.date) AS month,
            ROUND(SUM(CASE 
                WHEN CAST(s.total_weighted_landing_price AS String) ILIKE '%nan%' THEN 0
                ELSE s.total_weighted_landing_price 
            END), 2) AS total_sales
        FROM sales s
        INNER JOIN users_location ul ON s.customer_id = ul.customer_id
        WHERE ul.state_ut = '{state_ut}' 
        AND s.date BETWEEN '{from_date}' AND '{to_date}'
        GROUP BY month
        ORDER BY month
    """
    result = client.query(query)
    return [{"month": row[0], "total_sales": row[1]} for row in result.result_rows]

# Get top 5 products for a specific state/UT and month
def get_top_products_by_state_month(state_ut, month, from_date='2022-04-01', to_date='2022-06-30'):
    client = get_clickhouse_client()
    query = f"""
        SELECT 
            p.product_name, 
            ROUND(SUM(CASE 
                WHEN CAST(s.total_weighted_landing_price AS String) ILIKE '%nan%' THEN 0
                ELSE s.total_weighted_landing_price 
            END), 2) AS total_sales
        FROM sales s
        INNER JOIN products p ON s.product_id = p.product_id
        INNER JOIN users_location ul ON s.customer_id = ul.customer_id
        WHERE ul.state_ut = '{state_ut}' 
        AND EXTRACT(MONTH FROM s.date) = {month} 
        AND s.date BETWEEN '{from_date}' AND '{to_date}'
        GROUP BY p.product_name
        ORDER BY total_sales DESC
        LIMIT 5
    """
    result = client.query(query)
    return [{"product_name": row[0], "total_sales": row[1]} for row in result.result_rows]