from typing import List, Dict
from lexicon.lexicon import MESSAGES


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
