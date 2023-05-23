import logging

from databases import Database
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.sql import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from dotenv import load_dotenv
from typing import Tuple
import os

load_dotenv()

DATABASE_URL = os.environ['DATABASE_URL']
metadata = MetaData()

flights = Table(
    "flights",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("operator_code", String),
    Column("flight_number", String),
    Column("operator_name", String),
    Column("scheduled_time_of_departure", String),
    Column("estimated_time_of_departure", String),
    Column("arrival_or_departure", String),
    Column("location_code", String),
    Column("location_name", String),
    Column("location_name_hebrew", String),
    Column("location_name_translated", String),
    Column("location_country_hebrew", String),
    Column("location_country", String),
    Column("terminal", String),
    Column("checkin_counter", String),
    Column("checkin_zone", String),
    Column("remark_english", String),
    Column("remark_hebrew", String),
)

database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)


async def create_tables():
    metadata.create_all(engine)


async def insert_or_update_flight(flight_data) -> Tuple[int, int]:
    query = flights.select().where(flights.c.id == flight_data['id'])
    result = await database.fetch_one(query)

    new = 0
    updated = 0

    if result:
        diff = {k: (result[k], flight_data[k]) for k in flight_data if result[k] != flight_data[k]}
        if diff:
            update_query = flights.update().where(flights.c.id == flight_data['id']).values(**flight_data)
            await database.execute(update_query)
            updated = 1
            logging.info(f"Flight ID {flight_data['id']} updated. Old values: {diff}")
    else:
        insert_query = pg_insert(flights).values(**flight_data)
        await database.execute(insert_query)
        new = 1

    return new, updated


async def get_flight_by_condition(condition):
    if condition is None:
        query = select([flights])
    else:
        query = select([flights]).where(condition)

    return await database.fetch_all(query=query)
