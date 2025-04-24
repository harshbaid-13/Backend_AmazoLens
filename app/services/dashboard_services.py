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

def get_pie_chart_data(level, l0_category=None, l1_category=None, others_only=False):
    client = get_clickhouse_client()

    if level == 1 and not others_only:
        query = """
            SELECT l0_category, COUNT(*) as count 
            FROM products 
            GROUP BY l0_category 
            ORDER BY count DESC
        """
        result = client.query(query)
        all_rows = result.result_rows

        top_10 = all_rows[:10]
        others_total = sum(row[1] for row in all_rows[10:])
        
        results = [{"name": row[0], "value": row[1]} for row in top_10]
        if others_total > 0:
            results.append({"name": "Others", "value": others_total})
        return results

    elif level == 1 and others_only:
        query = """
            SELECT l0_category, COUNT(*) as count 
            FROM products 
            GROUP BY l0_category 
            ORDER BY count DESC
            OFFSET 10
        """
        result = client.query(query)
        return [{"name": row[0], "value": row[1]} for row in result.result_rows]

    elif level == 2 and l0_category:
        query = """
            SELECT l1_category, COUNT(*) as count 
            FROM products 
            WHERE l0_category = %(cat1)s 
            GROUP BY l1_category
        """
        result = client.query(query, {"cat1": l0_category})

    elif level == 3 and l0_category and l1_category:
        query = """
            SELECT l2_category, COUNT(*) as count 
            FROM products 
            WHERE l0_category = %(cat1)s AND l1_category = %(cat2)s 
            GROUP BY l2_category
        """
        result = client.query(query, {"cat1": l0_category, "cat2": l1_category})

    else:
        return []

    return [{"name": row[0], "value": row[1]} for row in result.result_rows]

def get_basic_data(month: str = "2022-06-01"):
    client = get_clickhouse_client()
    q_string=f"""
    SELECT 
        SUM(quantity) AS total_qty_sold,
        ROUND(SUM(total_weighted_landing_price),2) AS total_sales,
        ROUND(SUM(total_weighted_landing_price) / COUNT(DISTINCT order_id),2) AS avg_order_value,
        COUNT(DISTINCT customer_id) AS total_customers
    FROM 
        sales
    WHERE 
        toStartOfMonth(date) = toStartOfMonth(toDate('{str(month)}'))
    """
    result = client.query(q_string)
    data = {
        "total_qty_sold": result.result_rows[0][0],
        "total_sales": result.result_rows[0][1],
        "avg_order_value": result.result_rows[0][2],
        "total_customers": result.result_rows[0][3]
    }
    return data

def get_weekly_sales_data(start_date: str = "2022-04-01", end_date: str = "2022-06-30"):
    client = get_clickhouse_client()
    query = f"""
        SELECT 
            toStartOfWeek(s.date) AS week_start,
            SUM(s.quantity * s.unit_selling_price) AS total_sales
        FROM sales s
        WHERE s.date BETWEEN toDate('{start_date}') AND toDate('{end_date}')
        GROUP BY week_start
        ORDER BY week_start ASC
    """
    result = client.query(query)
    return [{"week": row[0].isoformat(), "sales": row[1]} for row in result.result_rows]
