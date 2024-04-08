import sys
import hashlib
import logging
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
