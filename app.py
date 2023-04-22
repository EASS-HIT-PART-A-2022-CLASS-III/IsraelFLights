import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Set the base URL for the FastAPI app
BASE_URL = "http://localhost:8000/"

# Define the endpoints and their corresponding titles
endpoints = {
    "Flights": "List of Flights",
    "Peak Hours": "Peak Hours of Departure",
    "Flight Status Counts": "Flight Status Counts",
    "Top Airlines": "Top Airlines by Number of Flights",
    "Busiest Routes": "Busiest Routes by Number of Flights",
    "Daily Average Delay": "Daily Average Delay in Minutes",
    "Weekly Average Delay": "Weekly Average Delay in Minutes",
}

# Set the page title and icon
st.set_page_config(page_title="Flight Tracker", page_icon=":airplane:")

# Set the sidebar title and options
st.sidebar.title("Flight Tracker")
selected_endpoint = st.sidebar.radio("Select an endpoint", list(endpoints.keys()))

# Make a GET request to the selected endpoint and display the response
st.title(endpoints[selected_endpoint])
response = requests.get(BASE_URL + selected_endpoint.lower().replace(" ", "_"))
if response.status_code == 200:
    data = response.json()
    if selected_endpoint == "Flights":
        # Convert the response data to a pandas DataFrame and display it in a table
        df = pd.DataFrame(data)
        st.dataframe(df)

    elif selected_endpoint == "Peak Hours":
        # Convert the response data to a pandas DataFrame and display it in a bar chart
        df = pd.DataFrame(data["peak_hours"], columns=["Hour", "Number of Flights"])
        fig = px.bar(df, x="Hour", y="Number of Flights", title="Peak Hours of Departure")
        st.plotly_chart(fig)

    elif selected_endpoint == "Flight Status Counts":
        # Convert the response data to a pandas DataFrame and display it in a pie chart
        df = pd.DataFrame(data, columns=["count", "status"])
        fig = px.pie(df, values="count", names="status", title="Flight Status Counts")
        st.plotly_chart(fig)

    elif selected_endpoint in ["Top Airlines", "Busiest Routes"]:
        # Convert the response data to a pandas DataFrame and display it in a bar chart
        df = pd.DataFrame(data, columns=["count", "destination" if selected_endpoint == "Busiest Routes" else "airline"])
        fig = px.bar(df, x="count", y="destination" if selected_endpoint == "Busiest Routes" else "airline", orientation="h", title=endpoints[selected_endpoint])
        st.plotly_chart(fig)

    elif selected_endpoint in ["Daily Average Delay", "Weekly Average Delay"]:
        # Display the average delay in minutes
        delay_minutes = data[selected_endpoint.lower().replace(" ", "_")]
        st.write(f"The {endpoints[selected_endpoint]} is {delay_minutes:.2f} minutes.")

else:
    st.write(f"Error: {response.status_code}")
