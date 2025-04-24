from app.dependencies.clickhouse import get_clickhouse_client
from prophet import Prophet
import pandas as pd


def get_top_products(limit=50):
    client = get_clickhouse_client()
    try:
        query = f"""
        SELECT 
            s.product_id,
            p.product_name,
            SUM(s.quantity) AS total_quantity
        FROM sales AS s
        JOIN products AS p ON s.product_id = p.product_id
        GROUP BY s.product_id, p.product_name
        ORDER BY total_quantity DESC
        LIMIT {limit}
        """
        result = client.query(query)
        return [
            {
                "product_id": row[0],
                "product_name": row[1]
            }
            for row in result.result_rows
        ]
    finally:
        client.close()


def get_forecast_for_product(product_id: int, granularity: str = "daily", days: int = 30):
    client = get_clickhouse_client()
    try:
        if granularity not in ["daily", "weekly"]:
            return {"error": "Invalid granularity. Choose 'daily' or 'weekly'."}

        if granularity == "daily":
            date_column = "toDate(date)"
            frequency = "D"
        else:
            date_column = "toStartOfWeek(toDate(date))"
            frequency = "W"

        name_result = client.query(f"""
            SELECT product_name FROM products WHERE product_id = {product_id} LIMIT 1
        """)
        product_name = name_result.result_rows[0][0] if name_result.result_rows else f"Product {product_id}"

        query = f"""
        SELECT 
            {date_column} AS period, 
            SUM(quantity) AS quantity
        FROM sales
        WHERE product_id = {product_id}
        GROUP BY period
        ORDER BY period
        """
        result = client.query(query)
        df = pd.DataFrame(result.result_rows, columns=["ds", "y"])

        if df.empty or len(df) < 10:
            return {"error": "Not enough data to forecast."}

        # Smoothing
        df["y"] = df["y"].rolling(window=7 if granularity == "daily" else 2, min_periods=1).mean()

        # Train Prophet
        model = Prophet(
            daily_seasonality=(granularity == "daily"),
            weekly_seasonality=(granularity == "weekly")
        )
        model.add_seasonality(name="monthly", period=30.5, fourier_order=5)
        model.fit(df)

        future = model.make_future_dataframe(periods=days, freq=frequency)
        forecast = model.predict(future)

        forecast["yhat"] = forecast["yhat"].clip(lower=0)
        forecast["yhat_lower"] = forecast["yhat_lower"].clip(lower=0)
        forecast["yhat_upper"] = forecast["yhat_upper"].clip(lower=0)

        last_actual_date = pd.to_datetime(df["ds"].max())

        response = []

        # Historical
        for _, row in df.iterrows():
            response.append({
                "date": str(row["ds"]),
                "value": round(row["y"], 2),
                "type": "actual",
                "product_name": product_name
            })

        # Forecast
        for _, row in forecast.iterrows():
            if row["ds"] > last_actual_date:
                response.append({
                    "date": str(row["ds"]),
                    "value": round(row["yhat"], 2),
                    "upper": round(row["yhat_upper"], 2),
                    "lower": round(row["yhat_lower"], 2),
                    "type": "forecast",
                    "product_name": product_name
                })

        return response

    finally:
        client.close()
