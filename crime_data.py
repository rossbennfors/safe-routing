#!/usr/bin/env python
# coding: utf-8

# In[39]:


import requests
import folium
from shapely.geometry import Polygon, Point
import geopandas as gpd
import osmnx as ox
from geopy.distance import geodesic

# Identify relevent crimes
pedestrian_crimes = [
    "anti-social-behaviour",
    "robbery",
    "violent-crime",
    "theft-from-the-person",
    "possession-of-weapons",
    "public-order"
]

# Give crimes weighing based on severity or relevance to pedestrian safety
crime_weights = {
    "anti-social-behaviour": 1,
    "robbery": 2,
    "violent-crime": 3,
    "theft-from-the-person": 1.5,
    "possession-of-weapons": 2.5,
    "public-order": 1
}

# Fetch Exeter's boundary as a GeoDataFrame
exeter = ox.geocode_to_gdf("Exeter, England")

# Get the boundary polygon 
boundary_polygon = exeter.geometry.iloc[0]

# Ensure the geometry is a polygon
if isinstance(boundary_polygon, Polygon):
     print("Geometry is a Polygon.")
else:
    print("Geometry is not a Polygon.")

# Simplify the polygon
simplified_polygon = boundary_polygon.simplify(0.001) 

# Convert the simplified polygon to a formatted string
simplified_exeter_boundary_coords = [(lat, lon) for lon, lat in simplified_polygon.exterior.coords]
simplified_exeter_boundary_poly = ':'.join([f"{lat},{lon}" for lat, lon in simplified_exeter_boundary_coords])

# Define the API endpoint
url = "https://data.police.uk/api/crimes-street/all-crime"

# Parameters for the API request
params = {"poly": simplified_exeter_boundary_poly}

# Make the API request
response = requests.post(url, data=params)

# Check if the request was successful
if response.status_code == 200:
    crimes = response.json() 
    print(f"Fetched {len(crimes)} crimes.")
else:
    print(f"Error: {response.status_code}")
    print(response.text)

# Filter crimes to only include pedestrian-related crime and add weight
filtered_crimes = [
        {
            "category": crime["category"],
            "latitude": float(crime["location"]["latitude"]),  
            "longitude": float(crime["location"]["longitude"]),  
            "weight": crime_weights.get(crime["category"], 1)  
        }
        for crime in crimes
        if crime["category"] in pedestrian_crimes  
    ]

# Function to calculate IDW score
def calculate_idw_score(selected_point, crimes, power=2, distance_threshold=100):
    """
    Calculate the IDW score for a selected point based on nearby crimes.
    
    Parameters:
        selected_point (tuple): The latitude and longitude of the selected point.
        crimes (list): A list of dictionaries, each containing 'latitude', 'longitude', and 'weight'.
        power (float): The power parameter for IDW. Default is 2.
    
    Returns:
        float: The calculated IDW score.
    """
    numerator = 0
    denominator = 0

    for crime in crimes:
        crime_point = (crime['latitude'], crime['longitude'])
        distance = geodesic(selected_point, crime_point).meters 
        
        # Skip crimes outside the distance threshold
        if distance > distance_threshold:
            continue
        print(f"Distance to crime: {distance:.2f} meters")
        if distance == 0:
            # Avoid division by zero; return max impact
            return crime.get('weight', 1)
        
        weight = crime.get('weight', 1)
        numerator += weight / (distance ** power)
        denominator += 1 / (distance ** power)

    return numerator / denominator if denominator != 0 else 0


# Test IDW function
selected_point = (50.725807, -3.526783) 

idw_score = calculate_idw_score(selected_point, filtered_crimes)
print(f"IDW Score for point {selected_point}: {idw_score}")






