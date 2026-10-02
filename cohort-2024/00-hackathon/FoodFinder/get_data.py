import requests
import os
import json
import math

API_KEY = os.getenv("GOOGLE_API_KEY")
ENDPOINT = "https://places.googleapis.com/v1/places:searchNearby"


def get_places_in_circle(latitude, longitude, radius, included_types=["restaurant"]):
    """Fetches places from Google Places API within a specified circle."""
    params = {
        "includedTypes": included_types,
        "rankPreference": "DISTANCE",
        "locationRestriction": {
            "circle": {
                "center": {"latitude": latitude, "longitude": longitude},
                "radius": radius,
            }
        },
    }

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": "places.displayName,places.id,places.location,places.types,places.businessStatus,places.currentOpeningHours,places.priceLevel,places.rating,places.userRatingCount,places.formattedAddress,places.photos,places.websiteUri,places.paymentOptions,places.dineIn,places.takeout,places.delivery,places.servesVegetarianFood,places.goodForGroups,places.parkingOptions,places.outdoorSeating",
    }
    try:
        response = requests.post(ENDPOINT, headers=headers, data=json.dumps(params))
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None


def create_grid_circles(center_lat, center_lon, total_radius, grid_radius):
    """Generates circle centers to cover a larger area with smaller circles."""

    circles = []
    # Create a bounding box for the larger circle
    lat_min = center_lat - (total_radius / 111111)
    lat_max = center_lat + (total_radius / 111111)
    lon_min = center_lon - (
        total_radius / (111111 * math.cos(math.radians(center_lat)))
    )
    lon_max = center_lon + (
        total_radius / (111111 * math.cos(math.radians(center_lat)))
    )

    # Calculate the number of grid cells in each direction (rough)
    num_lat = int((lat_max - lat_min) / (grid_radius / 111111) + 1)
    num_lon = int(
        (lon_max - lon_min)
        / (grid_radius / 111111 / math.cos(math.radians(center_lat)))
        + 1
    )

    # Calculate grid cell size
    d_lat = (lat_max - lat_min) / num_lat
    d_lon = (lon_max - lon_min) / num_lon

    for i in range(num_lat):
        for j in range(num_lon):
            lat = lat_min + i * d_lat
            lon = lon_min + j * d_lon
            circles.append((lat, lon))

    return circles


def main(center_lat=53.4609, center_lon=-2.2353, total_radius=2000, grid_radius=500):
    """Main function to fetch places using a grid of circles."""
    all_places = []
    grid_circles = create_grid_circles(
        center_lat, center_lon, total_radius, grid_radius
    )
    print(f"Created {len(grid_circles)} search circles.")

    for i, (lat, lon) in enumerate(grid_circles):
        print(
            f"Fetching results for grid cell {i+1}/{len(grid_circles)}: ({lat:.4f}, {lon:.4f})"
        )
        places_data = get_places_in_circle(lat, lon, grid_radius)
        if places_data and "places" in places_data:
            all_places.extend(places_data["places"])

    # Remove duplicate places based on place ID
    seen_ids = set()
    unique_places = []
    for place in all_places:
        if place["id"] not in seen_ids:
            seen_ids.add(place["id"])
            unique_places.append(place)
    all_places = unique_places

    with open("all_places_response.json", "w") as file:
        json.dump(all_places, file, indent=4)
    print(f"Total places found:{len(all_places)}")
    print("All place results saved to all_places_response.json")


if __name__ == "__main__":
    main()
