from datetime import datetime, timedelta
from typing import List, Dict


def process_session_data_user(sessions):
    session_list = [{
        'id': session[0],
        'session_start': session[1],
        'duration': session[2],
        'type_desc': session[3],
        'price': session[4]
    } for session in sessions]
    return session_list


def parse_datetime(date_time_str):
    try:
        return datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return None


def parse_session_data(session_data: dict):
    session_date_str = f'{session_data.get("date", "")} {session_data.get("time", "")}'
    duration = session_data.get('duration', 0)
    session_type = session_data.get('type', '')

    session_date = parse_datetime(session_date_str)

    if session_date is not None:
        session_end = session_date + timedelta(hours=duration)
    else:
        session_end = None

    return session_date, session_end, duration, session_type


def format_sessions_info(sessions: List[Dict[str, str]]) -> str:
    return "\n".join([
        f"Session ID: <b>{session['id']}</b>\n"
        f"Start Time: <b>{session['session_start'].split()[0]} | "
        f"{session['session_start'].split()[1][:5]}</b>\n"
        f"Duration: <b>{session['duration']}</b> hours\n"
        f"Session Type: <b>{session['type_desc']}</b>\n"
        f"Price: <b>{session['price']}</b>\n"
        for session in sessions
    ])
