import json
import folium

def visualize_places(json_file_path="all_places_response.json", output_html="places_map.html"):
    """
    Visualizes places from a JSON file on an interactive map.

    Args:
        json_file_path (str): Path to the JSON file containing places data.
        output_html (str): Path to save the generated HTML map file.
    """
    try:
        with open(json_file_path, 'r') as f:
            places = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at '{json_file_path}'")
        return
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{json_file_path}'")
        return


    # Calculate the center of all places for initial map view
    latitudes = [place['location']['latitude'] for place in places]
    longitudes = [place['location']['longitude'] for place in places]
    center_latitude = sum(latitudes) / len(latitudes) if latitudes else 0
    center_longitude = sum(longitudes) / len(longitudes) if longitudes else 0

    # Create a Folium map centered around the average location
    m = folium.Map(location=[center_latitude, center_longitude], zoom_start=12) # Adjust zoom_start as needed

    for place in places:
        location = place['location']
        display_name = place['displayName']['text']

        folium.Marker(
            location=[location['latitude'], location['longitude']],
            popup=display_name,
            tooltip=display_name  # Optional: tooltip on hover
        ).add_to(m)

    m.save(output_html)
    print(f"Map visualization saved to '{output_html}'")

if __name__ == "__main__":
    visualize_places() # Uses default file names: places_response.json and places_map.html
    # To use a different JSON file or output HTML file, you can call the function with arguments:
    # visualize_places(json_file_path="my_places.json", output_html="my_map.html")