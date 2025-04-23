import os
from app.dependencies.clickhouse import get_clickhouse_client
from fastapi import  HTTPException
from urllib.parse import unquote
import re
import pickle

def get_category():
    categories = set()
    directory= "public/market-basket"

    for filename in os.listdir(directory):
        # print(filename)
        
        categories.add(filename)

    return categories

def get_product_association_rules_service(category=""):
    try:
        query = f"""
        SELECT antecedents, consequents, confidence
        FROM product_association_rules
        WHERE category = '{str(category)}'
        ORDER BY confidence DESC
        """
        print(query)
        client = get_clickhouse_client()
        result = client.query(query)
        transformed = [
            {
                "antecedent": [item.strip() for item in row[0].split(",")],
                "consequent": [item.strip() for item in row[1].split(",")],
                "confidence": row[2]
            }
            for row in result.result_rows
        ]
        return transformed

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
def get_frequent_itemsets_service(category: str):
    try:
        # Query ClickHouse
        query = f"""
        SELECT itemsets, support,support_count
        FROM item_support_stats 
        WHERE category ='{str(category)}'
        """
        client = get_clickhouse_client()
        rows = client.query(query).result_rows
        # print(rows)
        
        result = []
        for itemset_str, support,support_count in rows:
            # Parse frozenset string like: "frozenset({'Atta', 'Arhar Dal'})"
            items = re.findall(r"'(.*?)'", itemset_str)
            if len(items) > 1:
                result.append({
                    "items": items,
                    "support": round(support, 6),
                    "support_count": round(support_count, 6)
                })

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

def get_heatmap_service(category=""):
    category = unquote(category)
    BASE_PATH = 'public/market-basket/' + category
    # print(BASE_PATH)

    heatmap_file = os.path.join(BASE_PATH, f"heatmap_output_{category}.csv")

    if not os.path.exists(heatmap_file):
        raise HTTPException(status_code=404, detail=f"Heatmap file for '{category}' not found.")

    try:
        # Read CSV without header, assuming first row is product names
        with open(heatmap_file, "r") as f:
            lines = f.readlines()
        
        # First line: product names
        product_names = [name.strip() for name in lines[0].strip().split(",")]

        # Remaining lines: heatmap values
        values = []
        for line in lines[1:]:
            row = [int(val.strip()) for val in line.strip().split(",")]
            values.append(row)

        return {
            "products": product_names,
            "values": values
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading heatmap files: {e}")
    
    
    
def get_sankey_service(category=""):
    category = unquote(category)
    BASE_PATH = 'public/market-basket/' + category
    # print(BASE_PATH)

    sankey_file = os.path.join(BASE_PATH, f"sankey_output_{category}.pkl")

    if not os.path.exists(sankey_file):
        raise HTTPException(status_code=404, detail=f"sankey file for '{category}' not found.")

    try:
        with open(sankey_file, 'rb') as handle:
            tree = pickle.load(handle)
        return tree

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading sankey files: {e}")
    
def get_fp_service(category=""):
    category = unquote(category)
    BASE_PATH = 'public/market-basket/' + category
    # print(BASE_PATH)

    fp_file = os.path.join(BASE_PATH, f"fp_output_{category}.pkl")

    if not os.path.exists(fp_file):
        raise HTTPException(status_code=404, detail=f"fp file for '{category}' not found.")

    try:
        with open(fp_file, 'rb') as handle:
            tree = pickle.load(handle)
        return tree

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading fp files: {e}")