import streamlit as st
import pandas as pd
import requests
import time

# Function to get place details
def get_place_details(place_id, fields=None):
    url = 'https://maps.googleapis.com/maps/api/place/details/json'
    params = {
        'place_id': place_id,
        'key': 'YOUR_API_KEY',
    }
    if fields:
        params['fields'] = ','.join(fields)
    response = requests.get(url, params=params)
    return response.json()

# Function to search places
def search_places(location, radius, place_type, max_results=100):
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    places = []
    params = {
        'location': location,
        'radius': radius,
        'type': place_type,
        'key': 'YOUR_API_KEY'
    }
    while len(places) < max_results:
        response = requests.get(url, params=params)
        data = response.json()
        places.extend(data['results'])
        if 'next_page_token' not in data:
            break
        params['pagetoken'] = data['next_page_token']
        time.sleep(2)  # Ensure enough delay before the next API call
    return places[:max_results]

# Streamlit code
st.title('Google Places Scraper')

# User inputs
location = st.text_input('Enter a location (latitude,longitude):')
radius = st.text_input('Enter a radius (in meters):')
place_type = st.text_input('Enter a place type:')

if st.button('Get Places'):
    # Get the places
    places = search_places(location, radius, place_type)

    # Get the details for each place
    details = []
    for place in places:
        detail = get_place_details(place['place_id'])
        if detail:
            details.append(detail)

    # Convert the details to a DataFrame
    df_details = pd.DataFrame(details)

    # Save the DataFrame to a CSV file
    df_details.to_csv('place_details.csv', index=False)

    st.write('The place details have been saved to place_details.csv.')
