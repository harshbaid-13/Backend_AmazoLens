from app.dependencies.clickhouse import get_clickhouse_client
import pandas as pd
from app.aryan_files.functions import make_folium_map
import datetime
def get_data():
    client = get_clickhouse_client()
    result = client.query("""
        SELECT * FROM sales
        LIMIT 1000
    """)
    return result.result_rows

def get_folium(from_date='2022-04-02', to_date='2022-04-02'):
    #print(type(str(from_date)))
    client = get_clickhouse_client()
    q_string=f"""  SELECT * FROM sales s inner join users_location ul on s.customer_id=ul.customer_id
where s.date>='{str(from_date)}' and s.date<='{str(to_date)}'
"""
    # print(q_string)
    result = client.query(q_string)
    sales=pd.DataFrame([row for row in result.result_rows])
    sales.columns=result.column_names

    map_str=make_folium_map(sales)
    return map_str 

def get_top_cities(from_date="", to_date=""):
    client = get_clickhouse_client()
    q_string=f"""SELECT 
            ul.state_ut, 
            ROUND(SUM(
                CASE 
                    WHEN CAST(s.total_weighted_landing_price AS String) ILIKE '%nan%' THEN 0
                    ELSE s.total_weighted_landing_price 
                END
            ),2) AS total_price
        FROM 
            (SELECT 
                customer_id, 
                total_weighted_landing_price, 
                date 
            FROM 
                sales 
            WHERE 
                date BETWEEN '{str(from_date)}' AND '{str(to_date)}') s 
        INNER JOIN 
            users_location ul ON s.customer_id = ul.customer_id 
        GROUP BY 
            ul.state_ut 
        ORDER BY 
            total_price DESC 
        LIMIT 10
    """
    result = client.query(q_string)
    return [{"state_ut": row[0], "total_price": row[1]} for row in result.result_rows]

