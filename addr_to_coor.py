import pandas as pd
import json
from mapbox import Geocoder

# Load the Excel file
data = pd.read_excel('科技執法.xlsm')

# Replace 'YOUR_MAPBOX_ACCESS_TOKEN' with your actual Mapbox Access Token
mapbox_access_token = 'pk.eyJ1IjoiZ2VyZTE2NTE1NiIsImEiOiJjbHAzZzhrcDcweGh5MnFtajZuN210cXVrIn0.0VsXgpoWSMdVPOIjN-f1XQ'
geocoder = Geocoder(access_token=mapbox_access_token)

# Transform the data into the required JSON format
json_list = []

for index, row in data.iterrows():
    road_name = row['properties.addr']

    # Use Mapbox Geocoding to get coordinates for the road
    try:
        response = geocoder.forward(road_name, limit=1)
        response.raise_for_status()  # Raise an exception for bad responses
        coordinates = response.json()['features'][0]['geometry']['coordinates']
    except Exception as e:
        # If geocoding fails, set coordinates to None and print the error
        coordinates = None
        print(f"Geocoding failed for road '{road_name}': {str(e)}")

    feature = {
        "type": "Feature",
        "properties": {
            "area": row['area'],  # Add additional properties as needed
            "type": row['type'],
            "func":row["func"],
            "direction":row["direction"],
            "addr":row["properties.addr"]
        },
        "geometry": {
            "type": "Point",
            "coordinates": coordinates if coordinates else []  # Use an empty list if coordinates is None
        }
    }
    json_list.append(feature)

# Create a GeoJSON feature collection
geojson_obj = {
    "type": "FeatureCollection",
    "crs": {
        "type": "name",
        "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}
    },
    "features": json_list
}

# Save the result into a GeoJSON file
output_filename = 'accident_equip.geojson'
with open(output_filename, 'w', encoding='utf-8') as f:
    json.dump(geojson_obj, f, ensure_ascii=False, indent=4)
