import sqlite3
import logging

# from config_data.config import load_config

DATABASE_FILE = 'users.db'
SESSIONS = 'garage_sessions'
TYPES = 'session_types'


class Database:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            # self.config = load_config()
            self.db_connection = None
            self._initialize_connection()
            self._initialized = True

    def _initialize_connection(self):
        if self.db_connection is None:
            try:
                logging.info("Creating a new database connection...")
                self.db_connection = sqlite3.connect(DATABASE_FILE)
                logging.info("Database connection created successfully.")
            except sqlite3.Error as e:
                logging.error(f"Error creating database connection: {e}.")

    def get_connection(self):
        if self.db_connection is not None:
            logging.info("Reusing existing database connection...")
            return self.db_connection
        else:
            self._initialize_connection()
            return self.db_connection

    def create_tables(self):
        try:
            with self.get_connection().cursor() as cur:
                cur.execute(f'''create table if not exists {SESSIONS} (
                                                id serial primary key,
                                                hashed_user_id text unique,
                                                src_lang text,
                                                dest_lang text
                                              )''')

                cur.execute(f'''create table if not exists {TYPES} (
                                                id serial primary key,
                                                hashed_user_id text,
                                                src_lang text,
                                                dest_lang text,
                                                created_at timestamp,
                                                foreign key (hashed_user_id) references {SESSIONS} (hashed_user_id)
                                              )''')
                self.db_connection.commit()
            logging.info(f"Database tables: «{SESSIONS}», «{TYPES}» created or verified.")
        except Exception as e:
            logging.error(f"Error initializing database: {e}.")

    def close_database(self):
        if self.db_connection:
            try:
                self.db_connection.close()
                logging.info("Database connection closed.")
            except Exception as e:
                logging.error(f"Error closing database connection: {e}.")
        else:
            logging.warning("No open database connection to close or connection is already closed.")
