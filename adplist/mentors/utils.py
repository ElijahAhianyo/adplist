import datetime

from django.conf import settings

import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd

Base = declarative_base()
from adplist.mentors.choices import SlotStatusChoiceTypes
# dbuser = settings.DB_USER
# dbpaswd = settings.DB_PASSWORD
# dbhost = settings.DB_HOST
# database = settings.DB_NAME
# port = settings.DB_PORT
DB_URL = settings.DATABASE_URL


def get_db_connection():
    try:
        engine = db.create_engine(DB_URL)  # Create test.sqlite automaticall
        metadata = db.MetaData()
        conn = engine.connect()
        return conn, engine
    except Exception as e:
        print("could not connect to database")


def format_datetime(date):
    return datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")





def create_slot(schedule):
    conn, engine = get_db_connection()
    minutes = 30
    days = 7
    columns = ['start', 'end', 'schedule_id']
    delta_minutes = datetime.timedelta(minutes=minutes)
    start_datetime = schedule.start
    end_datetime = schedule.end

    slot_count = int((end_datetime - start_datetime) / delta_minutes)
    seq = []

    for day in range(days):
        start, end = start_datetime, start_datetime + delta_minutes
        for i in range(slot_count):
            seq.append([start, end, schedule.pk])
            start, end = end, end + delta_minutes
        start_datetime = start_datetime + datetime.timedelta(hours=24)

    slots_df = pd.DataFrame(seq, columns=columns)
    slots_df["created_at"] = str(datetime.datetime.now())
    slots_df["updated_at"] = str(datetime.datetime.now())
    slots_df["status"] = SlotStatusChoiceTypes.FREE
    slots_df.to_sql('mentors_slot', con=engine, schema="public" ,if_exists='append', index=False)
    conn.close()
