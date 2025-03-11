from flask import Flask, render_template, request, redirect, url_for, jsonify
import math
import json
import pandas as pd
from ics_utils import *
import os
from werkzeug.utils import secure_filename
from datetime import datetime
import pytz

# --- Data Loading and Processing ---

def load_json_data(file_path):
    """Loads JSON data from a file."""
    with open(file_path, 'r') as f:
        return json.load(f)

def filter_operational_places(places):
    """Filters places to include only operational businesses."""
    return [place for place in places if place.get("businessStatus") == "OPERATIONAL"]

def create_extracted_attributes_map(extracted_attributes_list):
    """Creates a dictionary mapping place IDs to their extracted attributes."""
    return {item['id']: item for item in extracted_attributes_list}

def json_to_pandas_row(json_data):
    """Converts JSON data of a place into a Pandas DataFrame row."""
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
    """Creates a Pandas DataFrame from places data and extracted attributes."""
    if not places:
        return pd.DataFrame()

    assert len(places) == len(extracted_attributes), "Number of places and extracted attributes must match."

    df = json_to_pandas_row(places[0] | extracted_attributes[places[0]['id']])
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
    """Calculates the distance between two points on Earth using the Haversine formula."""
    R = 6371  # Radius of Earth in kilometers
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)

    a = math.sin(dLat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dLon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    return R * c

# --- Recommendation Engine ---

def get_restaurant_recommendations(df, cuisine_preference, spice_level, budget, distance, prev_lat, prev_lng, next_lat, next_lng):
    """Recommends restaurants based on user preferences and location."""
    if df.empty:
        print("DataFrame is empty. Please check data loading.")
        return [] # Return empty list instead of DataFrame
    print(prev_lat,prev_lng,next_lat,next_lng)
    if not prev_lat or not prev_lng or not next_lat or not next_lng:
        print("Location parameters are required.")
        return [] # Return empty list instead of DataFrame

    # 1. Distance Calculation
    df['distance_to'] = df.apply(
        lambda row: calculate_distance(
            float(prev_lat), float(prev_lng), row['latitude'], row['longitude']
        ), axis=1
    )
    df['distance_back'] = df.apply(
        lambda row: calculate_distance(
            float(next_lat), float(next_lng), row['latitude'], row['longitude']
        ), axis=1
    )
    df['distance_km'] = df['distance_to'] + df['distance_back']

    filtered_df = df.copy()

    # 2. Filtering

    # Distance Preference
    if distance and distance != "any":
        filtered_df = filtered_df[filtered_df['distance_km'] <= float(distance)]

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

    recommendations = []
    for index, row in filtered_df.head(10).iterrows():
        recommendations.append({
            'name': row['displayName_text'],
            'address': row['formattedAddress'],
            'types': row['types'],
            'rating': row['rating'],
            'userRatingCount': row['userRatingCount'],
            'distance_km': row['distance_km'],
            'restaurant_lat': row['latitude'], # Add restaurant lat
            'restaurant_lng': row['longitude'], # Add restaurant lng
            'prev_lat': float(prev_lat), # Add prev lat
            'prev_lng': float(prev_lng), # Add prev lng
            'next_lat': float(next_lat), # Add next lat
            'next_lng': float(next_lng)  # Add next lng
        })
    return recommendations


# --- Flask App ---

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'ics'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit for uploads

# Load data and create DataFrame outside of routes for efficiency
json_file_path = "all_places_response.json"
generated_content_path = "processed_places_response.json"

places_data = load_json_data(json_file_path)
operational_places = filter_operational_places(places_data)
extracted_attributes_list = load_json_data(generated_content_path)
extracted_attributes_map = create_extracted_attributes_map(extracted_attributes_list)
df = create_places_dataframe(operational_places, extracted_attributes_map)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def index():
    """Renders the index page with available cuisine options."""
    all_types_in_data = df['types'].str.split(', ', expand=True).stack().unique()
    available_cuisine_options = [
        cuisine for cuisine, types in cuisine_options_map.items()
        if any(item in all_types_in_data for item in types)
    ]
    return render_template('index.html', cuisine_options=available_cuisine_options, initial_lat=51.505, initial_lng=-0.09) # Default London

@app.route('/process_ics', methods=['POST'])
def process_ics_file():
    """Processes the uploaded ICS file and returns location data."""
    if 'ics_file' not in request.files:
        return jsonify({'error': 'No file part'})
    ics_file = request.files['ics_file']
    if ics_file.filename == '':
        return jsonify({'error': 'No selected file'})
    if ics_file and allowed_file(ics_file.filename):
        filename = secure_filename(ics_file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        ics_file.save(file_path)

        selected_date_input = request.form.get('selected_date')
        selected_time_input = request.form.get('selected_time')

        events = parse_ics(file_path)

        # Convert date and time inputs into a datetime object with timezone info
        selected_datetime_str = f"{selected_date_input} {selected_time_input}"
        selected_datetime = datetime.strptime(selected_datetime_str, "%Y-%m-%d %H:%M")
        selected_datetime = pytz.utc.localize(selected_datetime)

        (prev_lat, prev_lng), (next_lat, next_lng), next_start = get_lat_lng_from_events(events, selected_datetime)

        os.remove(file_path) # Clean up uploaded file

        return jsonify({
            'prev_lat': prev_lat,
            'prev_lng': prev_lng,
            'next_lat': next_lat,
            'next_lng': next_lng
        })
    return jsonify({'error': 'Invalid file type'})


@app.route('/recommend', methods=['POST'])
def recommend():
    """Handles the recommendation request and renders the results page."""
    if request.method == 'POST':
        cuisine_preference = request.form['cuisine_preference']
        spice_level = request.form.get('spice_level')
        budget = request.form.get('budget')
        distance = request.form.get('distance')
        print(distance)
        prev_lat = request.form.get('start_lat')
        prev_lng = request.form.get('start_lng')
        next_lat = request.form.get('end_lat')
        next_lng = request.form.get('end_lng')


        recommendations_list = get_restaurant_recommendations(
            df, cuisine_preference, spice_level, budget, distance, prev_lat, prev_lng, next_lat, next_lng
        )

        if recommendations_list:
            recommendations_df_for_table = pd.DataFrame(recommendations_list) # Create DataFrame for table
            recommendations_html = recommendations_df_for_table[['name', 'address', 'types', 'rating', 'userRatingCount', 'distance_km']].to_html(classes='table table-striped')
        else:
            recommendations_html = "<p>No recommendations found based on your criteria.</p>"

        return render_template('results.html', recommendations=recommendations_html, recommendations_data=recommendations_list)
    return render_template('index.html') # Handle GET request to /recommend


if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True, port=8080)