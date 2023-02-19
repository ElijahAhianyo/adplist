from config import celery_app
import datetime
from adplist.mentors.choices import SlotStatusChoiceTypes
from adplist.mentors.utils import get_db_connection
import pandas as pd

conn = get_db_connection()

@celery_app.task
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

