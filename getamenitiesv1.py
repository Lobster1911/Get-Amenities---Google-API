import pandas as pd
import requests
import time 

#Google Places API key
API_KEY = 'YOUR_API_KEY'

# City coordinates
latitude = 40.717745373463735
longitude = -74.00268403407253

# Define search parameters
radius = 35000  # radius in meters
keyword = ''  
type = ''  
language = 'en'

# Function to fetch places data
def fetch_places(url):
    places = []
    while True:
        response = requests.get(url).json()
        if 'results' in response:
            places.extend(response['results'])
        if 'next_page_token' not in response:
            break
        next_page_token = response['next_page_token']

        url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken={next_page_token}&key={API_KEY}'
        time.sleep(3)  # 3-second delay between requests
    return places

# Construct the initial API request URL
url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius={radius}&keyword={keyword}&type={type}&language={language}&key={API_KEY}'

# Fetch all places data
all_places = fetch_places(url)

# Parse the response and extract place information
if all_places:
    data = []
    for place in all_places:
        name = place['name']
        types = ', '.join(place['types'])
        address = place.get('vicinity', '')
        latitude = place['geometry']['location']['lat']
        longitude = place['geometry']['location']['lng']
        data.append([name, types, address, latitude, longitude])

    # Create a DataFrame from the data
    df = pd.DataFrame(data, columns=['Name', 'Types', 'Address', 'Latitude', 'Longitude'])

    # Export DataFrame to Excel
    excel_file = 'city_amenities.xlsx'
    df.to_excel(excel_file, index=False)
    print(f'Data saved to {excel_file}')
else:
    print('No results found.')
