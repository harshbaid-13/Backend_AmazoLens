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
