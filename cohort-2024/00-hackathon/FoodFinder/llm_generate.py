import google.generativeai as genai
import json
import time
import os
from tqdm import trange
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY) # Replace with your actual API key
def analyze_restaurants(restaurant_batch):
    """Analyzes a batch of restaurant data using the LLM to get spicy and price levels."""
    
    model = genai.GenerativeModel("gemini-2.0-flash-exp")
    batch_prompts = []
    
    for i, restaurant_data in enumerate(restaurant_batch):
        restaurant_name = restaurant_data.get("displayName", {}).get("text", "N/A")
        food_types = ", ".join(restaurant_data.get("types", []))
        additional_details = restaurant_data.get("formattedAddress", "") + ", " + ", ".join(restaurant_data.get("weekdayDescriptions", ""))

        batch_prompts.append(f"Restaurant {i+1}:\nRestaurant Name: {restaurant_name}\nFood Types: {food_types}\nAdditional Details: {additional_details}")

    user_prompt = "\n\n".join(batch_prompts)  # Combine all restaurant prompts

    full_prompt = f"{system_prompt}\n\n{user_prompt}"

    try:
        result = model.generate_content(
            full_prompt,
             generation_config=genai.GenerationConfig(
                 response_mime_type="application/json"
                )
        )
        if result.text:
            try:
              return json.loads(result.text)
            except json.JSONDecodeError:
              print(f"Error decoding JSON: {result.text}")
              return [{}] * len(restaurant_batch)
        else:
            return [{}] * len(restaurant_batch)
        
    except Exception as e:
        print(f"Error in API call: {e}")
        return [{}] * len(restaurant_batch)  # Handle API call error

system_prompt = """
You are an expert at analyzing restaurant descriptions to infer spicy and price levels.
Respond in JSON format as a list of objects, one for each restaurant in the same order as given.
Use the following enums:

enum PriceLevel {
    LOW = "Low Price",
    MEDIUM = "Medium Price",
    HIGH = "High Price",
    VERY_HIGH = "Very High Price"
}
enum SpicyLevel {
    NONE = "None",
    LOW = "Low",
    MEDIUM = "Medium",
    HIGH = "High",
    VERY_HIGH = "Very High"
}
Example output:
[
    {"spicy_level": "Medium", "price_level": "Medium Price"},
    {"spicy_level": "High", "price_level": "High Price"},
    ...
]
"""

def process_restaurant_data(places):
    """Processes restaurant data in batches of 10 and saves results."""
    processed_data = []
    
    for i in trange(0, len(places), 50):
        batch = places[i:i+50]
        spicy_price_data_list = analyze_restaurants(batch)
        
        for place, spicy_price_data in zip(batch, spicy_price_data_list):
            processed_data.append({"id": place.get("id"), **spicy_price_data})

        time.sleep(10)  # Avoid rate limiting

    return processed_data

json_file_path = "all_places_response.json"  # Replace with your actual path
output_json_file_path = "processed_places_response.json"

with open(json_file_path, "r") as f:
    places = json.load(f)
if os.path.exists(output_json_file_path):
    with open(output_json_file_path, "r") as f:
        existing_data = json.load(f)
    existing_ids = {item['id']: item for item in existing_data if item.get('spicy_level')}
    places = [place for place in places if place.get('id') not in existing_ids]
    if not places:
        print("All places already processed.")
        exit()

places = [place for place in places if place.get("businessStatus") == "OPERATIONAL"]

if places:
    processed_places = process_restaurant_data(places)
    if os.path.exists(output_json_file_path):
        non_empty_existing_data = [place for place in existing_data if place.get('spicy_level')]
        processed_places = non_empty_existing_data + processed_places
    with open(output_json_file_path, "w") as outfile:
        json.dump(processed_places, outfile, indent=4)
    print(f"Processed data saved to {output_json_file_path}")
else:
    print("The JSON list is empty.")