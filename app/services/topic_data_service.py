import calendar
from collections import Counter

import pandas as pd

from app.dependencies.clickhouse import get_clickhouse_client


def get_topic_data():
    client = get_clickhouse_client()
    result = client.query("""
        SELECT * FROM reviews
    """)

    df = pd.DataFrame(result.result_rows, columns=result.column_names)
    df = pd.read_csv("reviews_2025-04-21.csv", encoding="latin1")

    # Clean up: drop NAs and ensure string type
    df = df.dropna(subset=["final_l0_category", "name_of_topic", "review_title"])
    df["review_title"] = df["review_title"].astype(str)
    df["review_title"] = df["review_title"].str.replace(r"[^\w\s]", "", regex=True)

    # All categories to process (including "All")
    categories = ["All"] + sorted(df["final_l0_category"].unique())

    topicData = {}

    for category in categories:
        if category == "All":
            cat_df = df
        else:
            cat_df = df[df["final_l0_category"] == category]

        topic_list = []
        for topic, group in cat_df.groupby("name_of_topic"):
            # Aggregate all words for this topic
            words = group["review_title"].str.cat(sep=" ").lower().split()
            word_counts = Counter(words)
            # Take top 10 (or any number) most common words
            words_json = [
                {"text": word, "size": count}
                for word, count in word_counts.most_common(10)
            ]
            topic_list.append({"topic": topic, "words": words_json})
        topicData[category] = topic_list

    df["date_of_review"] = pd.to_datetime(df["date_of_review"], errors="coerce")
    df = df.dropna(subset=["date_of_review"])

    # Extract month as abbreviated name
    df["month"] = df["date_of_review"].dt.month
    df["month_str"] = df["month"].apply(lambda x: calendar.month_abbr[int(x)])

    topicTrends = []
    for topic, group in df.groupby("name_of_topic"):
        # Count reviews per month
        monthly_counts = (
            group.groupby("month_str")
            .size()
            .reindex(list(calendar.month_abbr)[1:], fill_value=0)
        )
        data = [
            {"month": month, "value": int(monthly_counts[month])}
            for month in list(calendar.month_abbr)[1:]
        ]
        topicTrends.append({"topic": topic, "data": data})

    return {
        "categories": categories,
        "topicData": topicData,
        "topicTrends": topicTrends,
    }
