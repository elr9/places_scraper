import streamlit as st
import pandas as pd
import requests
import time
import os
import io

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
        'key': 'AIzaSyAFfZJ9eGkYkS8nh5njzIx6qZpBB9aTfXo'
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
        detail = get_place_details(place['place_id'], ['name', 'formatted_address', 'formatted_phone_number', 'website'])
        if detail and 'result' in detail:
            details.append(detail['result'])

    # Convert the details to a DataFrame
    df_details = pd.DataFrame(details)

    # Convert the DataFrame to a CSV string
    csv = df_details.to_csv(index=False)
    csv_bytes = csv.encode()

    # Create a download button for the CSV file
    st.download_button(
        label="Download CSV file",
        data=csv_bytes,
        file_name='place_details.csv',
        mime='text/csv',
    )
