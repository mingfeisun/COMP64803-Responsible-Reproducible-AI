from flask import Flask, render_template, request
import math
import json
import pandas as pd

# --- Data Loading and Processing ---

def load_json_data(file_path):
    """Loads JSON data from a file.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        list or dict: Loaded JSON data.
    """
    with open(file_path, 'r') as f:
        return json.load(f)

def filter_operational_places(places):
    """Filters places to include only operational businesses.

    Args:
        places (list): List of place dictionaries.

    Returns:
        list: List of operational place dictionaries.
    """
    return [place for place in places if place.get("businessStatus") == "OPERATIONAL"]

def create_extracted_attributes_map(extracted_attributes_list):
    """Creates a dictionary mapping place IDs to their extracted attributes.

    Args:
        extracted_attributes_list (list): List of dictionaries containing extracted attributes.

    Returns:
        dict: Dictionary mapping place IDs to extracted attributes.
    """
    return {item['id']: item for item in extracted_attributes_list}

def json_to_pandas_row(json_data):
    """Converts JSON data of a place into a Pandas DataFrame row.

    Args:
        json_data (dict): JSON data for a single place.

    Returns:
        pd.DataFrame: DataFrame with a single row representing the place data.
    """
    data_row = {
        "id": json_data.get("id"),
        "types": ", ".join(json_data.get("types", [])),
        "formattedAddress": json_data.get("formattedAddress"),
        "latitude": json_data.get("location", {}).get("latitude"),
        "longitude": json_data.get("location", {}).get("longitude"),
        "rating": json_data.get("rating"),
        "businessStatus": json_data.get("businessStatus"),
        "userRatingCount": json_data.get("userRatingCount"),
        "displayName_text": json_data.get("displayName", {}).get("text"),
        "displayName_languageCode": json_data.get("displayName", {}).get("languageCode"),
        "takeout": json_data.get("takeout"),
        "delivery": json_data.get("delivery"),
        "dineIn": json_data.get("dineIn"),
        "openNow": json_data.get("currentOpeningHours", {}).get("openNow"),
        "weekdayDescriptions": "\n".join(json_data.get("currentOpeningHours", {}).get("weekdayDescriptions", [])),
        "acceptsCreditCards": json_data.get("paymentOptions", {}).get("acceptsCreditCards"),
        "acceptsDebitCards": json_data.get("paymentOptions", {}).get("acceptsDebitCards"),
        "acceptsCashOnly": json_data.get("paymentOptions", {}).get("acceptsCashOnly"),
        "acceptsNfc": json_data.get("paymentOptions", {}).get("acceptsNfc"),
        "freeParkingLot": json_data.get("parkingOptions", {}).get("freeParkingLot"),
        "freeStreetParking": json_data.get("parkingOptions", {}).get("freeStreetParking"),
        "spicyLevel": json_data.get("spicy_level"),
        "priceLevel": json_data.get("price_level")
    }
    return pd.DataFrame([data_row])

def create_places_dataframe(places, extracted_attributes):
    """Creates a Pandas DataFrame from places data and extracted attributes.

    Args:
        places (list): List of place dictionaries.
        extracted_attributes (dict): Dictionary of extracted attributes mapped by place ID.

    Returns:
        pd.DataFrame: DataFrame containing combined place data.
    """
    if not places:
        return pd.DataFrame()  # Return empty DataFrame if places list is empty

    assert len(places) == len(extracted_attributes), "Number of places and extracted attributes must match."

    df = json_to_pandas_row(places[0] | extracted_attributes[places[0]['id']]) # Merge dictionaries using | operator (Python 3.9+)
    for place in places[1:]:
        df = pd.concat([df, json_to_pandas_row(place | extracted_attributes[place['id']])], ignore_index=True)
    return df

# --- Cuisine Data ---

cuisine_options_map = {
    "American/Western/Cafe": ['american_restaurant', 'hamburger_restaurant', 'steak_house', 'barbecue_restaurant', 'diner', 'breakfast_restaurant', 'brunch_restaurant', 'buffet_restaurant', 'fast_food_restaurant', 'fine_dining_restaurant', 'food_court', 'sandwich_shop', 'deli', 'cafe', 'coffee_shop', 'tea_house', 'bar', 'pub', 'wine_bar', 'bar_and_grill'],
    "Italian": ['italian_restaurant', 'pizza_restaurant'],
    "Mexican": ['mexican_restaurant'],
    "Chinese": ['chinese_restaurant'],
    "Indian": ['indian_restaurant'],
    "Japanese": ['japanese_restaurant', 'sushi_restaurant', 'ramen_restaurant'],
    "Thai": ['thai_restaurant'],
    "Mediterranean/Middle Eastern/African": ['mediterranean_restaurant', 'greek_restaurant', 'lebanese_restaurant', 'turkish_restaurant', 'afghani_restaurant', 'middle_eastern_restaurant', 'african_restaurant', 'spanish_restaurant'],
    "Vietnamese": ['vietnamese_restaurant'],
    "Korean": ['korean_restaurant'],
    "Asian": ['asian_restaurant', 'indonesian_restaurant'],
    "Vegetarian/Vegan": ['vegan_restaurant', 'vegetarian_restaurant'],
    "Desserts/Bakery": ['dessert_restaurant', 'dessert_shop', 'bakery', 'bagel_shop', 'confectionery', 'ice_cream_shop', 'juice_shop'],
    "Seafood": ['seafood_restaurant'],
    "Other": ['restaurant', 'food']
}

# --- Distance Calculation ---

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculates the distance between two points on Earth using the Haversine formula.

    Args:
        lat1 (float): Latitude of the first point.
        lon1 (float): Longitude of the first point.
        lat2 (float): Latitude of the second point.
        lon2 (float): Longitude of the second point.

    Returns:
        float: Distance in kilometers.
    """
    R = 6371  # Radius of Earth in kilometers
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)

    a = math.sin(dLat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dLon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    return R * c

# --- Recommendation Engine ---

def get_restaurant_recommendations(df, cuisine_preference, user_latitude, user_longitude, spice_level, budget, max_distance_km):
    """Recommends restaurants based on user preferences.

    Args:
        df (pd.DataFrame): DataFrame of restaurant data.
        cuisine_preference (str): User's cuisine preference.
        user_latitude (str): User's latitude.
        user_longitude (str): User's longitude.
        spice_level (str): User's preferred spice level.
        budget (str): User's budget preference.
        max_distance_km (str): Maximum distance user is willing to travel.

    Returns:
        pd.DataFrame: DataFrame of recommended restaurants.
    """
    if df.empty:
        print("DataFrame is empty. Please check data loading.")
        return pd.DataFrame() # Return empty DataFrame

    # 1. Distance Calculation
    df['distance_km'] = df.apply(
        lambda row: calculate_distance(
            float(user_latitude), float(user_longitude), row['latitude'], row['longitude']
        ), axis=1
    )

    filtered_df = df.copy()

    # 2. Filtering
    # Cuisine Preference
    if cuisine_preference:
        types_to_filter = cuisine_options_map.get(cuisine_preference, [])
        if types_to_filter:
            filter_condition = filtered_df['types'].apply(lambda x: any(cuisine_type in x for cuisine_type in types_to_filter))
            filtered_df = filtered_df[filter_condition]

    # Spice Level
    if spice_level and spice_level != "":
        filtered_df = filtered_df[filtered_df['spicyLevel'] == spice_level]

    # Budget
    budget_mapping = {"Budget-friendly": 1, "Mid-range": 2, "Luxury": 3}
    if budget and budget != "":
        budget_level = budget_mapping.get(budget)
        filtered_df = filtered_df[filtered_df['priceLevel'] == budget_level]

    # 3. Sorting by rating (descending)
    if not filtered_df.empty:
        filtered_df = filtered_df.sort_values(by='rating', ascending=False, na_position='last')

    # 4. Return top recommendations
    return filtered_df[['displayName_text', 'formattedAddress', 'types', 'rating', 'userRatingCount', 'distance_km']].head(10)


# --- Flask App ---

app = Flask(__name__)

# Load data and create DataFrame outside of routes for efficiency (loaded once when app starts)
json_file_path = "all_places_response.json"
generated_content_path = "processed_places_response.json"

places_data = load_json_data(json_file_path)
operational_places = filter_operational_places(places_data)
extracted_attributes_list = load_json_data(generated_content_path)
extracted_attributes_map = create_extracted_attributes_map(extracted_attributes_list)
df = create_places_dataframe(operational_places, extracted_attributes_map)


@app.route('/', methods=['GET'])
def index():
    """Renders the index page with available cuisine options."""
    all_types_in_data = df['types'].str.split(', ', expand=True).stack().unique()
    available_cuisine_options = [
        cuisine for cuisine, types in cuisine_options_map.items()
        if any(item in all_types_in_data for item in types)
    ]
    return render_template('index.html', cuisine_options=available_cuisine_options)

@app.route('/recommend', methods=['POST'])
def recommend():
    """Handles the recommendation request and renders the results page."""
    if request.method == 'POST':
        cuisine_preference = request.form['cuisine_preference']
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        spice_level = request.form.get('spice_level')
        budget = request.form.get('budget')
        distance = request.form.get('distance') # Not used in current recommendation function

        recommendations_df = get_restaurant_recommendations(
            df, cuisine_preference, latitude, longitude, spice_level, budget, distance
        )

        if not recommendations_df.empty:
            recommendations_html = recommendations_df.to_html(classes='table table-striped') # Add Bootstrap styling
        else:
            recommendations_html = "<p>No recommendations found based on your criteria.</p>"

        return render_template('results.html', recommendations=recommendations_html)
    return render_template('index.html') # Handle GET request to /recommend


if __name__ == '__main__':
    app.run(debug=True, port=8080)