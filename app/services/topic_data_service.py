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
    df = df.dropna(subset=["split_2_category", "name_of_topic", "review_title"])
    df["review_title"] = df["review_title"].astype(str)
    df["review_title"] = df["review_title"].str.replace(r"[^\w\s]", "", regex=True)

    # All categories to process (including "All")
    categories = ["All"] + sorted(df["split_2_category"].unique())

    topicData = {}

    for category in categories:
        if category == "All":
            cat_df = df
        else:
            cat_df = df[df["split_2_category"] == category]

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

    # Ensure date_of_review is datetime
    df["date_of_review"] = pd.to_datetime(df["date_of_review"], errors="coerce")

    # Filter for months March (3) to July (7)
    df_filtered = df[df["date_of_review"].dt.month.between(3, 7)]

    # Create week start (Monday) column
    df_filtered["week_start"] = (
        df_filtered["date_of_review"].dt.to_period("W").apply(lambda r: r.start_time)
    )

    # Group by topic and week, count reviews
    weekly_counts = (
        df_filtered.groupby(["name_of_topic", "week_start"])
        .size()
        .reset_index(name="count")
    )

    # Get all weeks in the range (even if some weeks have 0 counts)
    all_weeks = pd.date_range(
        start=df_filtered["week_start"].min(),
        end=df_filtered["week_start"].max(),
        freq="W-MON",
    )
    all_weeks_str = all_weeks.strftime("%Y-%m-%d").tolist()

    topicTrends = []
    for topic, group in weekly_counts.groupby("name_of_topic"):
        week_count_dict = dict(
            zip(group["week_start"].dt.strftime("%Y-%m-%d"), group["count"])
        )
        # Fill missing weeks with 0
        data = [
            {
                "month": pd.to_datetime(week).strftime(
                    "%b %-d"
                ),  # 'Mar 3', 'Apr 7', etc.
                "value": int(week_count_dict.get(week, 0)),
            }
            for week in all_weeks_str
        ]
        topicTrends.append({"topic": topic, "data": data})

    return {
        "categories": categories,
        "topicData": topicData,
        "topicTrends": topicTrends,
    }
