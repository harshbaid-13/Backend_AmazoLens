from app.dependencies.clickhouse import get_clickhouse_client

def get_categories():
    client = get_clickhouse_client()
    try:
        result = client.query("""
            SELECT DISTINCT split_2_category 
            FROM reviews 
            ORDER BY split_2_category
        """)
        return [row[0] for row in result.result_rows]
    finally:
        client.close()

def get_overall_sentiment():
    client = get_clickhouse_client()
    try:
        result = client.query("SELECT ROUND(AVG(sentiment_score), 2) FROM reviews")
        return {"sentiment": result.result_rows[0][0]}
    finally:
        client.close()

def get_sentiment_trend():
    client = get_clickhouse_client()
    try:
        result = client.query("""
            SELECT 
                formatDateTime(toDate(parseDateTimeBestEffort(date_of_review)), '%b') AS month,
                toMonth(toDate(parseDateTimeBestEffort(date_of_review))) AS month_num,
                ROUND(AVG(sentiment_score), 2) AS sentiment
            FROM reviews
            GROUP BY month, month_num
            ORDER BY month_num
        """)
        return [{"month": row[0], "sentiment": row[2]} for row in result.result_rows]
    finally:
        client.close()

def get_sentiment_by_category():
    client = get_clickhouse_client()
    try:
        result = client.query("""
            SELECT
                split_2_category AS category,
                ROUND(SUM(sentiment = 'POSITIVE') * 100.0 / COUNT(), 1) AS positive,
                ROUND(SUM(sentiment = 'NEUTRAL') * 100.0 / COUNT(), 1) AS neutral,
                ROUND(SUM(sentiment = 'NEGATIVE') * 100.0 / COUNT(), 1) AS negative
            FROM reviews
            GROUP BY category
            ORDER BY category
        """)
        return {
            row[0]: {
                "positive": row[1],
                "neutral": row[2],
                "negative": row[3]
            }
            for row in result.result_rows
        }
    finally:
        client.close()

def get_recent_reviews(limit=5):
    client = get_clickhouse_client()
    try:
        result = client.query(f"""
            SELECT 
                review_title, 
                split_2_category, 
                sentiment, 
                date_of_review 
            FROM reviews
            ORDER BY date_of_review DESC
            LIMIT {limit}
        """)
        return [
            {
                "product": row[0],
                "category": row[1],
                "sentiment": row[2].lower(),
                "date": str(row[3])
            }
            for row in result.result_rows
        ]
    finally:
        client.close()
