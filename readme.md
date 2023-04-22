# Flight Status API

This is a RESTful API built using FastAPI that provides flight status information, including real-time updates, peak hours, and other useful statistics. The API retrieves data from the Israeli Ministry of Transportation's database.

## Features

- Retrieve flight information
- Register for flight status updates via email
- Get peak hours for flights
- Get flight status counts
- Get top airlines
- Get busiest routes
- Get daily and weekly average flight delays

## Installation

1. Clone this repository to your local machine.

```bash
git clone https://github.com/EASS-HIT-PART-A-2022-CLASS-III/IsraeliFlights.git
cd IsraeliFlights
```

2. Create and activate a virtual environment.

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install the required dependencies.

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory and populate it with the required environment variables.

```ini
DATABASE_URL=your_database_url
EMAIL_USERNAME=your_email_username
EMAIL_PASSWORD=your_email_password
EMAIL_HOST=your_email_host
EMAIL_PORT=your_email_port
```

5. Run the API using the following command:

```bash
uvicorn main:app --reload
```

6. To run the script that fetches and updates flight data periodically, execute:

```bash
python featch_flights_periodically.py
```

## Endpoints

1. `/flights` - Get all flights.
2. `/register` - Register for flight status updates via email.
3. `/peak_hours` - Get peak hours for flights.
4. `/flight_status_counts` - Get flight status counts.
5. `/top_airlines` - Get top airlines.
6. `/busiest_routes` - Get busiest routes.
7. `/daily_average_delay` - Get daily average flight delays.
8. `/weekly_average_delay` - Get weekly average flight delays.

## Usage

To use the API, send requests to the appropriate endpoints. For example:

```
http://localhost:8000/flights
```

## License

This project is licensed under the MIT License.