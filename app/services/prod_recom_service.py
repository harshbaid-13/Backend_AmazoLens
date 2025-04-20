import os

def get_category():
    prefix = "item_similarity_df_"
    suffix = ".parquet"
    categories = set()
    directory= "public/prod_recom"

    for filename in os.listdir(directory):
        #print(filename)
        if filename.startswith(prefix) and filename.endswith(suffix):
            category = filename[len(prefix):-len(suffix)]
            categories.add(category)

    return categories