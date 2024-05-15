import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor
import itertools

API_KEY = 'YOU_API_KEY'

# Read coordinates from Excel 
excel_file = r"D:\Gender Recognition (LSE)\coordinates.xlsx" #CHANGE_LOCATION
df_coordinates = pd.read_excel(excel_file)

# Define search parameters
radius = 300 
keyword = ''
type = ''
language = 'en'
base_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'

# Function to fetch places data for a given coordinate
def fetch_places(params):
    url = base_url + params
    response = requests.get(url).json()
    if 'results' in response:
        return response['results']
    return []

# Function to construct API request parameters
def construct_params(latitude, longitude):
    params = {
        'location': f'{latitude},{longitude}',
        'radius': radius,
        'keyword': keyword,
        'type': type,
        'language': language,
        'key': API_KEY
    }
    return '&'.join([f'{key}={value}' for key, value in params.items()])

# Accumulate all places data for each coordinate along with latitude and longitude
all_data = []
with ThreadPoolExecutor() as executor:
    coordinates = [(row['Latitude'], row['Longitude']) for index, row in df_coordinates.iterrows()]
    params_list = [construct_params(lat, lng) for lat, lng in coordinates]
    results = executor.map(fetch_places, params_list)

    for places, (latitude, longitude) in zip(results, coordinates):
        for place in places:
            name = place['name']
            types = ', '.join(place['types'])
            address = place.get('vicinity', '')
            lat = place['geometry']['location']['lat']
            lng = place['geometry']['location']['lng']
            all_data.append([latitude, longitude, name, types, address, lat, lng])
        # Add a blank row after each set of coordinates
        all_data.append([''] * len(all_data[0]))  # Add a row with empty values

# DataFrame 
df_all_data = pd.DataFrame(all_data, columns=['Latitude', 'Longitude', 'Name', 'Types', 'Address', 'Place Latitude', 'Place Longitude'])

# Export DataFrame to Excel
excel_file_output = r'D:\Gender Recognition (LSE)\all_places_data.xlsx' #CHANGE_LOCATION
df_all_data.to_excel(excel_file_output, index=False)
print(f'All places data saved to {excel_file_output}')
