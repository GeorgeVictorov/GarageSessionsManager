import logging
from datetime import datetime
from database.sqlite import Database

SESSIONS = 'garage_sessions'
TYPES = 'session_types'


def get_unavailable_times(selected_date):
    database = Database()
    conn = database.get_connection()
    try:
        cursor = conn.cursor()
        start_datetime = datetime.combine(selected_date, datetime.min.time())
        end_datetime = datetime.combine(selected_date, datetime.max.time())
        cursor.execute(
            f"SELECT session_start, session_end FROM {SESSIONS} WHERE session_start < ? AND ? < session_end",
            (end_datetime, start_datetime))
        unavailable_times = cursor.fetchall()
        cursor.close()
        logging.info("Successfully fetched unavailable times.")
        return unavailable_times
    except Exception as e:
        logging.error(f"An error occurred in get_available_time function: {str(e)}.")

# def get_unavailable_time(session_start, session_end):
#     database = Database()
#     conn = database.get_connection()
#     try:
#         cursor = conn.cursor()
#         cursor.execute(
#             f"SELECT COUNT(*) FROM {SESSIONS} WHERE session_start < ? AND ? < session_end",
#             (session_end, session_start))
#         unavailable = cursor.fetchone()[0]
#         cursor.close()
#         logging.info("Successfully fetched unavailable hours.")
#         return unavailable
#     except Exception as e:
#         logging.error(f"An error occurred in get_available_time function: {str(e)}.")
