import logging
from datetime import datetime
from database.sqlite import Database

SESSIONS = 'garage_sessions'
TYPES = 'session_types'


def admin_canceled_info(session_id: int) -> tuple:
    database = Database()
    conn = database.get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(f'''
                        select s.session_start, s.duration, t.type_desc
                        from {SESSIONS} s
                        inner join {TYPES} t on s.type = t.id
                        where s.id = ?
                    ''', (session_id,))
        sessions_info = cursor.fetchone()
        cursor.close()
        logging.info('Successfully retrieved sessions info.')
        return sessions_info

    except Exception as e:
        logging.error(f"An error occurred in admin_canceled_info function: {str(e)}.")


def admin_upcoming_sessions() -> list:
    database = Database()
    conn = database.get_connection()
    try:
        cursor = conn.cursor()
        today = datetime.now().date()
        cursor.execute(f'''
                    select s.id, s.user_username, s.session_start, s.duration, t.type_desc, 
                    t.price * s.duration, is_payed
                    from {SESSIONS} s
                    inner join {TYPES} t on s.type = t.id
                    where s.session_start >= ? and  s.is_canceled = 0
                    order by 3
                ''', (today,))
        sessions = cursor.fetchall()
        cursor.close()
        session_list = []
        for session in sessions:
            session_dict = {
                'id': session[0],
                'username': session[1],
                'session_start': session[2],
                'duration': session[3],
                'type_desc': session[4],
                'total_price': session[5],
                'is_payed': session[6]
            }
            session_list.append(session_dict)
        logging.info('Successfully retrieved sessions info.')
        return session_list
    except Exception as e:
        logging.error(f"An error occurred in admin_upcoming_sessions function: {str(e)}.")


def admin_unpaid_sessions() -> list:
    database = Database()
    conn = database.get_connection()
    try:
        cursor = conn.cursor()
        today = datetime.now().date()
        cursor.execute(f'''
                    select s.id, s.user_username, s.session_start, s.duration, t.type_desc, 
                    t.price * s.duration
                    from {SESSIONS} s
                    inner join {TYPES} t on s.type = t.id
                    where s.session_start >= ? and  s.is_canceled = 0 and is_payed = 0
                    order by 3
                ''', (today,))
        sessions = cursor.fetchall()
        cursor.close()
        session_list = []
        for session in sessions:
            session_dict = {
                'id': session[0],
                'username': session[1],
                'session_start': session[2],
                'duration': session[3],
                'type_desc': session[4],
                'total_price': session[5]
            }
            session_list.append(session_dict)
        logging.info('Successfully retrieved sessions info.')
        return session_list
    except Exception as e:
        logging.error(f"An error occurred in admin_unpaid_sessions function: {str(e)}.")


def admin_confirm_session_payment(session_id: int):
    database = Database()
    conn = database.get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(f'update {SESSIONS} set is_payed = 1 where id = ?', (session_id,))
        conn.commit()
        cursor.close()
        logging.info("Payment confirmed.")
    except Exception as e:
        logging.error(f"An error occurred in admin_payment function: {str(e)}.")


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
