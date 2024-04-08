import logging
from database.db import Database

SESSIONS = 'garage_sessions'
TYPES = 'session_types'
USERS = 'garage_users'
PAYMENTS = 'sessions_payment'


def get_sessions_history():
    database = Database()
    conn = database.get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(f'''
            select
                sessions.id as "Session ID",
                sessions.user_username as "Username",
                sessions.session_start as "Start time",
                sessions.session_end as "End time",
                types.type_desc as "Type",
                case
                    when is_payed = true then 'Payed'
                    else 'Not payed'
                end as "Payment",
                case
                    when sessions.is_canceled = true then 'Canceled'
                    else 'OK'
                end as "Status",
                payments.total_price as "Payed amount",
                payments.payed_on as "Payment date"
            from {SESSIONS} sessions
            inner join {TYPES} types on sessions.type = types.id
            left outer join {PAYMENTS} payments on sessions.id = payments.session_id
            order by 3''')
            rows = cursor.fetchall()
            cols = [description[0] for description in cursor.description]
            logging.info("Retrieved sessions history from the database.")
            return cols, rows
    except Exception as e:
        logging.error(f"Error getting sessions history from the database: {e}.")
        return None, None


def get_type_prices():
    database = Database()
    conn = database.get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(f'select type_desc, price from {TYPES} order by id')
            type_prices = cursor.fetchall()
            logging.info("Retrieved prices from the database.")
            return type_prices
    except Exception as e:
        logging.error(f"Error getting prices from the database: {e}.")


def get_users():
    database = Database()
    conn = database.get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(f'''
            select user_id, user_username, phone_number,
            case
                when is_banned = true then 'User is banned'
                else 'Not banned'
            end as ban 
            from {USERS} order by id''')
            type_prices = cursor.fetchall()
            logging.info("Retrieved users from the database.")
            return type_prices
    except Exception as e:
        logging.error(f"Error getting users from the database: {e}.")
