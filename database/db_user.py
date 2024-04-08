import logging
from datetime import datetime
from database.db import Database
from services.user import process_session_data_user

SESSIONS = 'garage_sessions'
TYPES = 'session_types'
USERS = 'garage_users'


def get_unavailable_times(selected_date):
    database = Database()
    conn = database.get_connection()
    try:
        with conn.cursor() as cursor:
            start_datetime = datetime.combine(selected_date, datetime.min.time())
            end_datetime = datetime.combine(selected_date, datetime.max.time())
            cursor.execute(
                f'''select 
                to_char(session_start, 'YYYY-MM-DD HH24:MI:SS'), 
                to_char(session_end, 'YYYY-MM-DD HH24:MI:SS')
                from {SESSIONS} 
                where session_start < %s and %s < session_end and
                is_canceled = false''',
                (end_datetime, start_datetime))
            unavailable_times = cursor.fetchall()
            logging.info("Successfully fetched unavailable times.")
            return unavailable_times
    except Exception as e:
        logging.error(f"An error occurred in get_available_time function: {str(e)}.")


def book_new_session(*args):
    database = Database()
    conn = database.get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                f'''insert into {SESSIONS} (user_id, user_username, session_start, session_end, duration, type)
                    values (%s, %s, %s, %s, %s, %s)''', args)
            conn.commit()
        logging.info("Successfully booked a session.")
    except Exception as e:
        logging.error(f"An error occurred in book_new_session function: {str(e)}.")
        conn.rollback()


def upcoming_sessions(user_id: int) -> list:
    database = Database()
    conn = database.get_connection()
    try:
        with conn.cursor() as cursor:
            today = datetime.now().date()
            cursor.execute(f'''
                        select s.id, to_char(s.session_start, 'YYYY-MM-DD HH24:MI:SS'), s.duration, t.type_desc, 
                        case
                            when is_payed = false then t.price * s.duration
                            else 0
                        end
                        from {SESSIONS} s
                        inner join {TYPES} t on s.type = t.id
                        where s.session_start >= %s and user_id = %s and s.is_canceled = false
                        order by 2
                    ''', (today, user_id))
            sessions = cursor.fetchall()
            session_list = process_session_data_user(sessions)
            logging.info('Successfully retrieved sessions info.')
            return session_list
    except Exception as e:
        logging.error(f"An error occurred in upcoming_sessions function: {str(e)}.")


def cancel_session(session_id: int):
    database = Database()
    conn = database.get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(f'update {SESSIONS} set is_canceled = true where id = %s', (session_id,))
            conn.commit()
            logging.info("Successfully canceled a session.")
    except Exception as e:
        logging.error(f"An error occurred in cancel_session function: {str(e)}.")
        conn.rollback()


def change_user_number(user_id: int, new_number: str):
    database = Database()
    conn = database.get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"update {USERS} set phone_number = %s where user_id = %s", (new_number, user_id))
            conn.commit()

            cursor.execute(f"select phone_number from {USERS} where user_id = %s", (user_id,))
            row = cursor.fetchone()
            if row:
                user_number = row[0]
                logging.info(f"Changed phone number for user_id {user_id} successfully.")
                return user_number
            else:
                logging.error(f"No user found with user_id {user_id}.")
                return None
    except Exception as e:
        logging.error(f"An error occurred while changing the phone number: {str(e)}")
        conn.rollback()
        return None
