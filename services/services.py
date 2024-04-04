from datetime import datetime


class SessionManager:
    def __init__(self):
        self.sessions = {}

    def get_session(self, user_id):
        return self.sessions.get(user_id, {})

    def set_session(self, user_id, session_data):
        self.sessions[user_id] = session_data


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

    return session_date, duration, session_type
