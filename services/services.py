class SessionManager:
    def __init__(self):
        self.sessions = {}

    def get_session(self, user_id):
        return self.sessions.get(user_id, {})

    def set_session(self, user_id, session_data):
        self.sessions[user_id] = session_data
