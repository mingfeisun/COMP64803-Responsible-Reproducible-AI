from flask import Flask, render_template, request
import math
import json
import pandas as pd
from get_pandas import json_to_pandas_row
from sentence_transformers import SentenceTransformer

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():

    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    if request.method == 'POST':
        date = request.form['date']
        time = request.form['time']
        cuisine_preference = request.form['cuisine_preference'] # Updated name
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        allergies_list = request.form.getlist('allergies') # Use getlist for multiple select
        spice_level = request.form.get('spice_level') # Use get to handle optional fields gracefully
        budget = request.form.get('budget') # Use get to handle optional fields gracefully
        distance = request.form.get('distance') # Use get to handle optional fields gracefully


        # **Call your recommendation algorithm here**
        # Pass all parameters to your algorithm
        recommendations = get_restaurant_recommendations(
            date, time, cuisine_preference, latitude, longitude,
            allergies_list, spice_level, budget, distance # Pass new parameters
        )

        return render_template('results.html', recommendations=recommendations) # Create results.html next

    return render_template('index.html')

def update_score(key, places, threshold=0.1):
    """
    Updates the score based on the given key and places.
    Args:
        key (str): The key representing the score to be updated.
        places (dict): A dictionary of places with the key and score to be updated.
        threshold (float): The threshold value for updating the score.
    Returns:
        places(dict): A dictionary of places with the updated score.
    """
    # get embedding of the key
    model = SentenceTransformer("all-MiniLM-L6-v2")
    key_embedding = model.encode(key)
    # compare key embedding with each embedding of place["type"] for each place in places, take the max
    places[key+"_score"] = places['embeddings'].apply(lambda x: max([model.similarity(t,key_embedding) for t in x]))
    # if score is greater than threshold, update the score of the place, otherwise remove the place from places
    places = places[places[key+"_score"] >= threshold]
    # TODO should save the scores in json for future use
    return places

def apply_filters(df, soft_filter=False, **filters):
    """
    Apply filters to the DataFrame of places.

    Args:
        df (pd.DataFrame): DataFrame containing places data.
        filters (dict): Key-value pairs to filter places by specific fields.
        soft_filter (bool): If True, apply soft filtering by updating scores.

    Returns:
        pd.DataFrame: Filtered DataFrame.
    """
    if not soft_filter:
        for key, value in filters.items():
            if isinstance(value, list):
                df = df[df[key].isin(value)]
            else:
                df = df[df[key] == value]
        return df
    else:
        for _, value in filters.items():
            df = update_score(value, df, threshold=soft_filter)
        return df

def update_distance(places, lat1, lon1):
    for place in places:
        lat2 = place['location']['latitude']
        lon2 = place['location']['longitude']
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.asin(math.sqrt(a))

        # Radius of Earth in meters.
        r = 6371 * 1000
        c * r
        place['distance'] = c * r
    return places

def get_restaurant_recommendations(date, time, cuisine_preference, latitude, longitude, allergies, spice_level, budget, distance):
    """
    This is a placeholder for your restaurant recommendation algorithm.
    Replace this with your actual algorithm logic.
    """
    # For now, just return some dummy data based on food type
    print(date, time, cuisine_preference, latitude, longitude)
    json_file_path = "all_places_response.json"
    try:
        with open(json_file_path, 'r') as f:
            places = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at '{json_file_path}'")
        return
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{json_file_path}'")
        return
    places = apply_filters(places, {'businessStatus': 'OPERATIONAL', 'priceLevel': ['PRICE_LEVEL_EXPENSIVE','PRICE_LEVEL_MODERATE', 'PRICE_LEVEL_INEXPENSIVE']})
    places = update_distance(places, latitude, longitude)
    # TODO apply a hard filter that distance < remaining travel time * speed
    df = json_to_pandas_row(places[0])
    # TODO remove irrelavant columns beforehand
    # append remaining rows
    for place in places[1:]:
        df = pd.concat([df, json_to_pandas_row(place)], ignore_index=True)
    df = apply_filters(df, food_type=cuisine_preference, soft_filter=0.1)
    score_columns = [col for col in df.columns if col.endswith('_score')]
    df['relevance_score'] = df[score_columns].sum(axis=1)
    # TODO better way to calculate overall score
    df["overall_score"] = df["relevance_score"] * (df["rating"] * df["userRatingCount"]) / df["distance"]
    df = df[df['relevance_score'] >= 0.5] # threshold can be adjusted
    # sort by overall_score
    df = df.sort_values(by='overall_score', ascending=False)
    return df

if __name__ == '__main__':
    app.run(debug=True, port=8080)