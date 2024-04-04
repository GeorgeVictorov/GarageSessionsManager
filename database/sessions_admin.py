import logging
from datetime import datetime
from database.sqlite import Database

SESSIONS = 'garage_sessions'
TYPES = 'session_types'


def admin_upcoming_sessions() -> list:
    database = Database()
    conn = database.get_connection()
    try:
        cursor = conn.cursor()
        today = datetime.now().date()
        cursor.execute(f'''
                    select s.id, s.session_start, s.duration, t.type_desc
                    from {SESSIONS} s
                    inner join {TYPES} t on s.type = t.id
                    where s.session_start >= ? and  s.is_canceled = 0
                    order by 2
                ''', (today,))
        sessions = cursor.fetchall()
        cursor.close()
        session_list = []
        for session in sessions:
            session_dict = {
                'id': session[0],
                'session_start': session[1],
                'duration': session[2],
                'type_desc': session[3]
            }
            session_list.append(session_dict)
        logging.info('Successfully retrieved sessions info.')
        return session_list
    except Exception as e:
        logging.error(f"An error occurred in upcoming_sessions function: {str(e)}.")


def admin_cancel_session(session_id: int):
    database = Database()
    conn = database.get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(f'update {SESSIONS} set is_canceled = 1 where id = ?', (session_id,))
        conn.commit()
        cursor.close()
        logging.info("Successfully canceled a session.")
    except Exception as e:
        logging.error(f"An error occurred in upcoming_sessions function: {str(e)}.")