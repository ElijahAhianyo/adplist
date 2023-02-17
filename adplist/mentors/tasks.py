from config import celery_app
import datetime
from adplist.mentors.choices import SlotStatusChoiceTypes
from adplist.mentors.utils import get_db_connection
import pandas as pd

conn = get_db_connection()

@celery_app.task
def create_slot(data):
    minutes = 30
    days = 7
    columns = ['start', 'end', 'schedule']
    delta_minutes = datetime.timedelta(minutes=minutes)
    start_datetime = datetime.datetime.strptime(data['start'], "%Y-%m-%dT%H:%M:%SZ")
    end_datetime = datetime.datetime.strptime(data['start'], "%Y-%m-%dT%H:%M:%SZ")

    slot_count = int((end_datetime - start_datetime) / delta_minutes)
    seq = []

    for day in range(days):
        start, end = start_datetime, start_datetime + delta_minutes
        for i in range(slot_count):
            seq.append([start, end, data["schedule"]])
            start, end = end, end + delta_minutes
        start_datetime= start_datetime + datetime.timedelta(hours=24)

    slots_df = pd.DataFrame(seq, columns=columns)
    slots_df.to_sql('booking_slots_db', con=conn, if_exists='append', index=False)

