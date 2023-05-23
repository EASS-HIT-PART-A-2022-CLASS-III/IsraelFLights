# Israel Flights Tracker

This project is designed to fetch and display real-time flight information for flights in and out of Israel. It consists of a backend API built with FastAPI, a frontend built with Streamlit, a PostgreSQL database for storing flight data, and a Python script that fetches flight data periodically.

## Project Structure

- `./backend` - Contains the FastAPI application.
- `./frontend` - Contains the Streamlit application.
- `fetch_flights_periodically.py` - Python script to fetch flight data periodically.

## Prerequisites

- Docker and Docker Compose installed on your machine.

## Installation

1. Clone the repository to your local machine.

2. From the project root, run the following command to build and start all services:

```shell
docker-compose up --build -d
```

## Accessing the Applications
* The FastAPI backend can be accessed at http://localhost:8000.
* The Streamlit frontend can be accessed at http://localhost:8501.

## Environment Variables
The following environment variables are used in this project:

* DATABASE_URL: The connection string for the PostgreSQL database.
* BASE_URL: The base URL for the backend API.