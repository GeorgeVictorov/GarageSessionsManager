import logging
from datetime import datetime
from cachetools import cached, TTLCache
from database.db import Database
from services.admin import process_session_data_admin

SESSIONS = 'garage_sessions'
TYPES = 'session_types'
USERS = 'garage_users'
PAYMENTS = 'sessions_payment'

cache = TTLCache(maxsize=100, ttl=300)


def clear_cache():
    cache.clear()
    logging.info("Cached users cleared.")


def admin_canceled_info(session_id: int) -> tuple:
    database = Database()
    conn = database.get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(f'''
                            select s.session_start, s.duration, t.type_desc
                            from {SESSIONS} s
                            inner join {TYPES} t on s.type = t.id
                            where s.id = %s
                        ''', (session_id,))
            sessions_info = cursor.fetchone()
            logging.info('Successfully retrieved sessions info.')
            return sessions_info

    except Exception as e:
        logging.error(f"An error occurred in admin_canceled_info function: {str(e)}.")


def admin_upcoming_sessions() -> list:
    database = Database()
    conn = database.get_connection()
    try:
        with conn.cursor() as cursor:
            today = datetime.now().date()
            cursor.execute(f'''
                        select s.id, s.user_username, to_char(s.session_start, 'YYYY-MM-DD HH24:MI:SS'), 
                        s.duration, t.type_desc, t.price * s.duration, is_payed
                        from {SESSIONS} s
                        inner join {TYPES} t on s.type = t.id
                        where s.session_start >= %s and s.is_canceled = false
                        order by 3
                    ''', (today,))
            sessions = cursor.fetchall()
            session_list = process_session_data_admin(sessions)
            logging.info('Successfully retrieved sessions info.')
            return session_list
    except Exception as e:
        logging.error(f"An error occurred in admin_upcoming_sessions function: {str(e)}.")


def admin_unpaid_sessions() -> list:
    database = Database()
    conn = database.get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(f'''
                        select s.id, s.user_username, to_char(s.session_start, 'YYYY-MM-DD HH24:MI:SS'), 
                        s.duration, t.type_desc, t.price * s.duration, is_payed
                        from {SESSIONS} s
                        inner join {TYPES} t on s.type = t.id
                        where s.is_canceled = false and is_payed = false
                        order by 3
                    ''')
            sessions = cursor.fetchall()
            session_list = process_session_data_admin(sessions)
            logging.info('Successfully retrieved sessions info.')
            return session_list
    except Exception as e:
        logging.error(f"An error occurred in admin_unpaid_sessions function: {str(e)}.")


def admin_confirm_session_payment(session_id: int):
    database = Database()
    conn = database.get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(f'update {SESSIONS} set is_payed = true where id = %s', (session_id,))
            cursor.execute(f'''
                        insert into {PAYMENTS} (session_id, total_price)
                        values (%s, (
                                    select 
                                    type.price * session.duration 
                                    from {SESSIONS} session 
                                    inner join {TYPES} type on session.type = type.id
                                    where session.id = %s))''',
                           (session_id, session_id))
            conn.commit()
            logging.info("Payment confirmed.")
    except Exception as e:
        logging.error(f"An error occurred in admin_payment function: {str(e)}.")
        conn.rollback()


def admin_cancel_session(session_id: int):
    database = Database()
    conn = database.get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(f'update {SESSIONS} set is_canceled = true where id = %s', (session_id,))
            conn.commit()
        logging.info("Successfully canceled a session.")
    except Exception as e:
        logging.error(f"An error occurred in upcoming_sessions function: {str(e)}.")
        conn.rollback()


def update_types_price(type_id: int, new_price: int):
    database = Database()
    conn = database.get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"update {TYPES} set price = %s where id = %s", (new_price, type_id))
            conn.commit()

            cursor.execute(f"select type_desc, price from {TYPES} where id = %s", (type_id,))
            type_desc = cursor.fetchone()[0]

            logging.info(f"Price for session ID {type_id} updated successfully.")
            return type_desc
    except Exception as e:
        logging.error(f"An error occurred while updating price: {str(e)}")
        conn.rollback()
        return None


def admin_ban_or_unban_user(user_id: int, action: str):
    database = Database()
    conn = database.get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(f'update {USERS} set is_banned = %s where user_id = %s', (action, user_id,))
            conn.commit()

            cursor.execute(f'select is_banned from {USERS} where user_id = %s', (user_id,))
            status = cursor.fetchone()[0]

            logging.info("Successfully updated user status a session.")
            return status
    except Exception as e:
        logging.error(f"An error occurred in admin_ban_or_unban_user function: {str(e)}.")
        conn.rollback()


@cached(cache=cache)
def admin_user_status(user_id: int):
    database = Database()
    conn = database.get_connection()
    try:
        with conn.cursor() as cursor:
            logging.debug(f"Executing SQL query: select is_banned from {USERS} where user_id = %s")
            cursor.execute(f'select is_banned from {USERS} where user_id = %s', (user_id,))
            status = cursor.fetchone()
            if status is not None:
                status = status[0]
                logging.info("Successfully fetched user status.")
                return status
            else:
                logging.info("No status found for the user.")
                return 0
    except Exception as e:
        logging.error(f"An error occurred in admin_user_status function: {str(e)}.")
