import sys
import hashlib
import logging
from datetime import datetime, timedelta
from typing import List, Dict
from database.db import Database


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


def hash_file_data(data: str) -> str:
    try:
        file_hash = hashlib.sha256()
        for line in data:
            file_hash.update(line.encode('utf-8'))
        logging.info("Hashed file data successfully")
        return file_hash.hexdigest()
    except Exception as e:
        logging.error(f"Error hashing file data: {e}")


def sigterm_handler():
    db_instance = Database()
    try:
        logging.info("SIGTERM received. Shutting down...")
        db_instance.close_database()
        sys.exit(0)
    except Exception as e:
        logging.error(f"Error in sigterm_handler: {e}")
        sys.exit(1)


def sigint_handler():
    db_instance = Database()
    try:
        logging.info("Received SIGINT signal. Shutting down...")
        db_instance.close_database()
        sys.exit(0)
    except Exception as e:
        logging.error(f"Error in sigint_handler: {e}")
        sys.exit(1)
