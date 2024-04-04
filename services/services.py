from datetime import datetime, timedelta


class SessionManager:
    def __init__(self):
        self.sessions = {}

    def get_session(self, user_id):
        return self.sessions.get(user_id, {})

    def set_session(self, user_id, session_data):
        self.sessions[user_id] = session_data

    def clear_session(self, user_id):
        if user_id in self.sessions:
            del self.sessions[user_id]


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
