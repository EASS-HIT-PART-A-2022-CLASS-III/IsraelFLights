import os

import streamlit as st
import requests
import pandas as pd

BASE_URL = os.environ.get('BASE_URL')

st.set_page_config(
    page_title="Israeli Flight Statistics",
    page_icon=":airplane:",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title('Israeli Flight Statistics')

st.sidebar.header('Menu')
options = ['View Flights', 'Register Flight Status Update', 'Peak Hours', 'Flight Status Counts', 'Top Airlines', 'Busiest Routes', 'Average Delay']
choice = st.sidebar.selectbox("Choose an option", options)

if choice == 'View Flights':
    st.header('Flights')
    res = requests.get(f'{BASE_URL}/flights')
    data = res.json()
    df = pd.DataFrame(data)
    st.dataframe(df)

elif choice == 'Register Flight Status Update':
    st.header('Register for Flight Status Update')
    email = st.text_input("Enter your email")
    flight_number = st.text_input("Enter flight number")
    if st.button("Register"):
        res = requests.post(f'{BASE_URL}/register', json={"email": email, "flight_number": flight_number})
        if res.status_code == 200:
            st.success('Registered successfully!')
        else:
            st.error('Registration failed.')

elif choice == 'Peak Hours':
    st.header('Peak Hours')
    res = requests.get(f'{BASE_URL}/peak_hours')
    data = res.json()
    for idx, hour in enumerate(data['peak_hours'], start=1):
        st.subheader(f"Peak Hour {idx}")
        st.write(f"Hour: {hour[0]}")
        st.write(f"Count: {hour[1]}")

elif choice == 'Flight Status Counts':
    st.header('Flight Status Counts')
    res = requests.get(f'{BASE_URL}/flight_status_counts')
    data = res.json()
    df = pd.DataFrame(data)
    st.dataframe(df)

elif choice == 'Top Airlines':
    st.header('Top Airlines')
    res = requests.get(f'{BASE_URL}/top_airlines')
    data = res.json()
    df = pd.DataFrame(data)
    st.dataframe(df)

elif choice == 'Busiest Routes':
    st.header('Busiest Routes')
    res = requests.get(f'{BASE_URL}/busiest_routes')
    data = res.json()
    df = pd.DataFrame(data)
    st.dataframe(df)

elif choice == 'Average Delay':
    st.header('Average Delay')
    daily_delay_res = requests.get(f'{BASE_URL}/daily_average_delay')
    daily_delay_data = daily_delay_res.json()
    st.write(f"Daily Average Delay: {daily_delay_data['daily_average_delay']} minutes")

    weekly_delay_res = requests.get(f'{BASE_URL}/weekly_average_delay')
    weekly_delay_data = weekly_delay_res.json()
    st.write(f"Weekly Average Delay: {weekly_delay_data['weekly_average_delay']} minutes")
