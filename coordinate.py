import pandas as pd
import json

# Load the Excel file
data = pd.read_excel('accident_hot.xlsm')

# Transform the data into the required JSON format
json_list = []
for index, row in data.iterrows():
    feature = {
        "type": "Feature",
        "properties": {
            "count": row['count'],
            "addr": row['properties.addr'],
            "area": row["area"]
        },
        "geometry": {
            "type": "Point",
            "coordinates": [row['Longitude'], row['Latitude']]
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
output_filename = 'accident_hot.geojson'
with open(output_filename, 'w', encoding='utf-8') as f:
    json.dump(geojson_obj, f, ensure_ascii=False, indent=4)
