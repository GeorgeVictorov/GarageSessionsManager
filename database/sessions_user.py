import logging
from datetime import datetime
from database.sqlite import Database

SESSIONS = 'garage_sessions'
TYPES = 'session_types'
USERS = 'garage_users'


def get_unavailable_times(selected_date):
    database = Database()
    conn = database.get_connection()
    try:
        cursor = conn.cursor()
        start_datetime = datetime.combine(selected_date, datetime.min.time())
        end_datetime = datetime.combine(selected_date, datetime.max.time())
        cursor.execute(
            f'''select session_start, session_end from {SESSIONS} 
            where session_start < ? and ? < session_end and
            is_canceled = 0''',
            (end_datetime, start_datetime))
        unavailable_times = cursor.fetchall()
        cursor.close()
        logging.info("Successfully fetched unavailable times.")
        return unavailable_times
    except Exception as e:
        logging.error(f"An error occurred in get_available_time function: {str(e)}.")


def book_new_session(*args):
    database = Database()
    conn = database.get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            f'''insert into {SESSIONS} (user_id, user_username, session_start, session_end, duration, type)
                values (?, ?, ?, ?, ?, ?)''', args)
        conn.commit()
        cursor.close()
        logging.info("Successfully booked a session.")
    except Exception as e:
        logging.error(f"An error occurred in book_new_session function: {str(e)}.")


def upcoming_sessions(user_id: int) -> list:
    database = Database()
    conn = database.get_connection()
    try:
        cursor = conn.cursor()
        today = datetime.now().date()
        cursor.execute(f'''
                    select s.id, s.session_start, s.duration, t.type_desc, 
                    case
                        when is_payed = 0 then t.price * s.duration
                        else "Payed"
                    end
                    from {SESSIONS} s
                    inner join {TYPES} t on s.type = t.id
                    where s.session_start >= ? and user_id = ? and s.is_canceled = 0
                    order by 2
                ''', (today, user_id))
        sessions = cursor.fetchall()
        cursor.close()
        session_list = []
        for session in sessions:
            session_dict = {
                'id': session[0],
                'session_start': session[1],
                'duration': session[2],
                'type_desc': session[3],
                'price': session[4]
            }
            session_list.append(session_dict)
        logging.info('Successfully retrieved sessions info.')
        return session_list
    except Exception as e:
        logging.error(f"An error occurred in upcoming_sessions function: {str(e)}.")


def cancel_session(session_id: int):
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


def change_user_number(user_id: int, new_number: str):
    database = Database()
    conn = database.get_connection()
    try:
        cursor = conn.cursor()

        cursor.execute(f"update {USERS} set phone_number = ? where user_id = ?", (new_number, user_id))
        conn.commit()

        cursor.execute(f"select phone_number from {USERS} where user_id = ?", (user_id,))
        row = cursor.fetchone()
        cursor.close()
        if row:
            user_number = row[0]
            logging.info(f"Changed phone number for user_id {user_id} successfully.")
            return user_number
        else:
            logging.error(f"No user found with user_id {user_id}.")
            return None
    except Exception as e:
        logging.error(f"An error occurred while changing the phone number: {str(e)}")
        return None
