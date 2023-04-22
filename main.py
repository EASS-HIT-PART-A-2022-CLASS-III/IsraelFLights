from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from database import database, create_tables, get_flight_by_condition, flights
from datetime import datetime, date, timedelta
from sqlalchemy import func, select, and_, Integer
from email_util import send_email
from collections import Counter

app = FastAPI()
security = HTTPBasic()


class Flight(BaseModel):
    id: int
    operator_code: str
    flight_number: str
    operator_name: str
    scheduled_time_of_departure: str
    estimated_time_of_departure: str
    arrival_or_departure: str
    location_code: str
    location_name: str
    location_name_hebrew: str
    location_name_translated: str
    location_country_hebrew: str
    location_country: str
    terminal: str
    checkin_counter: Optional[str] = None
    checkin_zone: Optional[str] = None
    remark_english: str
    remark_hebrew: str


def map_flight_data(flight):
    return {
        'id': flight['_id'],
        'operator_code': flight['CHOPER'],
        'flight_number': flight['CHFLTN'],
        'operator_name': flight['CHOPERD'],
        'scheduled_time_of_departure': flight['CHSTOL'],
        'estimated_time_of_departure': flight['CHPTOL'],
        'arrival_or_departure': flight['CHAORD'],
        'location_code': flight['CHLOC1'],
        'location_name': flight['CHLOC1D'],
        'location_name_hebrew': flight['CHLOC1TH'],
        'location_name_translated': flight['CHLOC1T'],
        'location_country_hebrew': flight['CHLOC1CH'],
        'location_country': flight['CHLOCCT'],
        'terminal': flight['CHTERM'],
        'checkin_counter': flight['CHCINT'],
        'checkin_zone': flight['CHCKZN'],
        'remark_english': flight['CHRMINE'],
        'remark_hebrew': flight['CHRMINH'],
    }


@app.on_event("startup")
async def startup_event():
    await database.connect()
    await create_tables()


@app.on_event("shutdown")
async def shutdown_event():
    await database.disconnect()


@app.get("/flights", response_model=List[Flight])
async def get_flights():
    flights_data = await get_flight_by_condition(None)
    return flights_data


class FlightStatusNotification(BaseModel):
    email: EmailStr
    flight_number: str


@app.post("/register")
async def register_flight_status_update(notification: FlightStatusNotification,
                                        credentials: HTTPBasicCredentials = Depends(security)):
    flight_data = await get_flight_by_condition(flights.c.flight_number.ilike(f"%{notification.flight_number}%"))

    if not flight_data:
        raise HTTPException(status_code=404, detail="Flight not found")

    flight = flight_data[0]
    subject = f"Flight Status Update: {flight['flight_number']}"
    content = f"Your flight {flight['flight_number']} operated by {flight['operator_name']} is scheduled to depart at {flight['scheduled_time_of_departure']} and the current estimated departure time is {flight['estimated_time_of_departure']}."

    send_email(subject, content, notification.email)

    return {"detail": "Flight status update email sent successfully"}


def filter_flights_current_day(flights):
    current_day_flights = []
    today = date.today()
    for flight in flights:
        scheduled_time = datetime.strptime(flight['scheduled_time_of_departure'], '%Y-%m-%dT%H:%M:%S')
        if scheduled_time.date() == today:
            current_day_flights.append(flight)
    return current_day_flights


def group_flights_by_hour(flights):
    hours_count = Counter()
    for flight in flights:
        scheduled_time = datetime.strptime(flight['scheduled_time_of_departure'], '%Y-%m-%dT%H:%M:%S')
        hours_count[scheduled_time.hour] += 1
    return hours_count


@app.get("/peak_hours")
async def get_peak_hours():
    flights_data = await get_flights()
    current_day_flights = filter_flights_current_day(flights_data)
    hours_count = group_flights_by_hour(current_day_flights)
    peak_hours = sorted(hours_count.items(), key=lambda x: x[1], reverse=True)[:3]
    return {"peak_hours": peak_hours}


@app.get("/flight_status_counts")
async def get_flight_status_counts():
    query = (
        select([
            func.count().label("count"),
            flights.c.remark_english.label("status"),
        ])
        .where(flights.c.remark_english.in_(["DEPARTED", "LANDED", "NOT FINAL", "ON TIME", "CANCELED"]))
        .group_by(flights.c.remark_english)
    )
    flight_status_counts = await database.fetch_all(query=query)
    return flight_status_counts



@app.get("/top_airlines")
async def get_top_airlines():
    query = (
        select([
            func.count().label("count"),
            flights.c.operator_name.label("airline"),
        ])
        .group_by(flights.c.operator_name)
        .order_by(func.count().desc())
        .limit(5)
    )
    top_airlines = await database.fetch_all(query=query)
    return top_airlines


@app.get("/busiest_routes")
async def get_busiest_routes():
    query = (
        select([
            func.count().label("count"),
            flights.c.location_name.label("destination"),
        ])
        .group_by(flights.c.location_name)
        .order_by(func.count().desc())
        .limit(5)
    )
    busiest_routes = await database.fetch_all(query=query)
    return busiest_routes


def calculate_flight_delay(flight):
    scheduled_time = datetime.strptime(flight['scheduled_time_of_departure'], '%Y-%m-%dT%H:%M:%S')
    estimated_time = datetime.strptime(flight['estimated_time_of_departure'], '%Y-%m-%dT%H:%M:%S')
    delay = estimated_time - scheduled_time
    delay_minutes = delay.total_seconds() / 60
    return delay_minutes


@app.get("/daily_average_delay")
async def get_daily_average_delay():
    flights_data = await get_flights()
    current_day_flights = filter_flights_current_day(flights_data)
    delays = [calculate_flight_delay(flight) for flight in current_day_flights]
    daily_average_delay = sum(delays) / len(delays) if delays else 0
    return {"daily_average_delay": daily_average_delay}


def is_current_week(date_to_check):
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    return start_of_week <= date_to_check <= end_of_week


def filter_flights_current_week(flights):
    current_week_flights = []
    for flight in flights:
        scheduled_time = datetime.strptime(flight['scheduled_time_of_departure'], '%Y-%m-%dT%H:%M:%S')
        if is_current_week(scheduled_time.date()):
            current_week_flights.append(flight)
    return current_week_flights


@app.get("/weekly_average_delay")
async def get_weekly_average_delay():
    flights_data = await get_flights()
    weekly_flights = filter_flights_current_week(flights_data)
    delays = [calculate_flight_delay(flight) for flight in weekly_flights]
    weekly_average_delay = sum(delays) / len(delays) if delays else 0
    return {"weekly_average_delay": weekly_average_delay}
