import io
import csv
import logging
from datetime import datetime
from database.sqlite import Database
from services.services import hash_file_data

SESSIONS = 'garage_sessions'
TYPES = 'session_types'


def get_sessions_history():
    database = Database()
    conn = database.get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(f'''
        select
            sessions.id as "Session ID",
            sessions.user_username as "Username",
            sessions.session_start as "Start time",
            sessions.session_end as "End time",
            types.type_desc as "Type",
            case
                when is_payed = 1 then sessions.duration * types.price
                else "Not payed"
            end as "Payment",
            case
                when sessions.is_canceled = 1 then "Canceled"
                else ""
            end as "Status"
        from {SESSIONS} sessions
        inner join {TYPES} types on sessions.type = types.id
        order by 3''')
        rows = cursor.fetchall()
        cols = [description[0] for description in cursor.description]
        cursor.close()
        logging.info("Retrieved sessions from the database.")
        return cols, rows

    except Exception as e:
        logging.error(f"Error getting sessions from the database: {e}.")
        return None, None


def history_to_csv(columns, data):
    try:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(columns)
        writer.writerows(data)
        csv_data = output.getvalue()
        logging.info("Converted sessions to CSV successfully.")
        return csv_data
    except (io.UnsupportedOperation, csv.Error) as e:
        logging.error(f"Error converting sessions to CSV: {e}.")
        return None


def generate_filename(data):
    try:
        data_to_hash = [','.join(map(str, row)) for row in data]
        hashed_data = hash_file_data('\n'.join(data_to_hash))[-4:]
        current_date = datetime.now().strftime('%Y-%m-%d')
        file_name = f'session_history_{current_date}_{hashed_data}.csv'
        logging.info("Generated filename for stats data.")
        return file_name
    except Exception as e:
        logging.error(f"Error generating filename for stats data: {e}.")
        return None


def get_type_prices():
    database = Database()
    conn = database.get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(f'select type_desc, price from {TYPES} order by id')
        type_prices = cursor.fetchall()
        logging.info("Retrieved prices from the database.")
        return type_prices
    except Exception as e:
        logging.error(f"Error getting prices from the database: {e}.")
