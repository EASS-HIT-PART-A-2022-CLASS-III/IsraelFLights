import streamlit as st
import requests

# Fetch data from the API
def get_data(endpoint):
    response = requests.get(f"http://localhost:8000/{endpoint}")
    return response.json()

# Display the information
st.title("Airport Dashboard")

flights_last_day = get_data("flights/last_day_count")
flights_expected = get_data("flights/expected_count")
delayed_flights = get_data("flights/delayed_count")

st.write(f"Flights in the last 24 hours: {flights_last_day}")
st.write(f"Expected flights in the next 24 hours: {flights_expected}")
st.write(f"Delayed flights: {delayed_flights}")

# Display rush hour information
rush_hours = "Morning (6AM-9AM) and Evening (5PM-8PM)"  # Update this based on your data analysis
st.write(f"Expected rush hours: {rush_hours}")
