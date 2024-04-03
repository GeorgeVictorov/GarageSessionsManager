import logging
from database.sqlite import Database

SESSIONS = 'garage_sessions'
TYPES = 'session_types'


def get_unavailable_time(session_start, session_end):
    database = Database()
    conn = database.get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT COUNT(*) FROM {SESSIONS} WHERE session_start < ? AND ? < session_end",
            (session_end, session_start))
        unavailable = cursor.fetchone()[0]
        cursor.close()
        logging.info("Successfully fetched unavailable hours.")
        return unavailable
    except Exception as e:
        logging.error(f"An error occurred in get_available_time function: {str(e)}.")
