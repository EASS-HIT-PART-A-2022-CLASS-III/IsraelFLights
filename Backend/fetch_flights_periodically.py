import asyncio
import httpx
from main import map_flight_data
from database import database, insert_or_update_flight, create_tables
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)

load_dotenv()

API_URL = f"https://data.gov.il/api/3/action/datastore_search?resource_id=e83f763b-b7d7-479e-b172-ae981ddc6de5"


async def fetch_all_flights():
    async with httpx.AsyncClient() as client:
        params = {'limit': 3000000}
        response = await client.get(API_URL, params=params)
        data = response.json()
        flight_records = data['result']['records']
        flights = [map_flight_data(flight) for flight in flight_records]
        return flights


async def update_database():
    flights = await fetch_all_flights()
    new_rows = 0
    updated_rows = 0

    for flight in flights:
        new, updated = await insert_or_update_flight(flight)
        new_rows += new
        updated_rows += updated

    logging.info(f"New rows added: {new_rows}, Rows updated: {updated_rows}")


async def fetch_flights_periodically():
    await database.connect()
    await create_tables()
    try:
        while True:
            logging.info("Updating database...")
            await update_database()
            await asyncio.sleep(60*15)  # 60 seconds
    finally:
        await database.disconnect()


if __name__ == "__main__":
    asyncio.run(fetch_flights_periodically())

