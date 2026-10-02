import json
import pandas as pd
from get_pandas import json_to_pandas_row
from sentence_transformers import SentenceTransformer

def get_embeddings(model, input_json_file_path="all_places_response.json", output_json_file_path="all_places_response_with_embeddings.json"):
    with open(input_json_file_path, 'r') as f:
        places = json.load(f)

    if places:
        # Initialize an empty DataFrame with the first row
        df = json_to_pandas_row(places[0])
        
        # Append remaining rows
        for place in places[1:]:
            df = pd.concat([df, json_to_pandas_row(place)], ignore_index=True)
        df["embeddings"] = df["types"].apply(lambda x: [model.encode(t) for t in x])
        df.to_json(output_json_file_path, orient='records', lines=True)

if __name__ == "__main__":
    model = SentenceTransformer("all-MiniLM-L6-v2")
    get_embeddings(model)