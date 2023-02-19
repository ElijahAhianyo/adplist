import datetime

from django.conf import settings

import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

DB_URL = settings.DATABASE_URL


def get_db_connection():
    try:
        engine = db.create_engine(DB_URL)  # Create test.sqlite automaticall
        metadata = db.MetaData()
        conn = engine.connect()
        return conn, engine
    except Exception as e:
        print("could not connect to database")

