import io
import csv
import logging
from datetime import datetime
from typing import List, Dict
from lexicon.lexicon import MESSAGES
from services.services import hash_file_data


def format_sessions(booked_sessions: List[Dict[str, str]]) -> str:
    if not booked_sessions:
        return "<b>There are no upcoming sessions.</b>"

    sessions_info = "\n".join([
        format_sessions_info(user_session)
        for user_session in booked_sessions
    ])
    return MESSAGES['/admin_upcoming'].format(sessions_info)


def format_sessions_info(user_session: Dict[str, str]) -> str:
    session_start_time = user_session['session_start'].split()[1][:5]
    is_payed = "Yes" if user_session['is_payed'] == 1 else "No"
    return (
        f"Session ID: <b>{user_session['id']}</b>\n"
        f"Username: <b>{user_session['username']}</b>\n"
        f"Start Time: <b>{user_session['session_start'].split()[0]} | {session_start_time}</b>\n"
        f"Duration: <b>{user_session['duration']}</b> hours\n"
        f"Session Type: <b>{user_session['type_desc']}</b>\n"
        f"Total price: <b>{user_session['total_price']}</b>\n"
        f"Is payed: <b>{is_payed}</b>\n\n"
    )


def process_session_data_admin(sessions):
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
    return session_list


def history_to_csv(columns, data):
    try:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(columns)
        writer.writerows(data)
        csv_data = output.getvalue()
        logging.info("Converted sessions history to CSV successfully.")
        return csv_data
    except (io.UnsupportedOperation, csv.Error) as e:
        logging.error(f"Error converting sessions history to CSV: {e}.")
        return None


def generate_filename(data):
    try:
        data_to_hash = [','.join(map(str, row)) for row in data]
        hashed_data = hash_file_data('\n'.join(data_to_hash))[-4:]
        current_date = datetime.now().strftime('%Y-%m-%d')
        file_name = f'session_history_{current_date}_{hashed_data}.csv'
        logging.info("Generated filename for sessions history.")
        return file_name
    except Exception as e:
        logging.error(f"Error generating filename for sessions history: {e}.")
        return None
