import sqlite3
import logging

DATABASE_FILE = 'database/garage.db'
SESSIONS = 'garage_sessions'
TYPES = 'session_types'
USERS = 'garage_users'


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
            cur = self.get_connection().cursor()
            cur.execute(f'''create table if not exists {SESSIONS} (
                                                id integer primary key,
                                                user_id int,
                                                user_username text,
                                                session_start datetime,
                                                session_end datetime,
                                                duration int,
                                                type int,
                                                is_payed boolean default false,
                                                is_canceled boolean default false
                                              )''')

            cur.execute(f'''create table if not exists {TYPES} (
                                                id serial primary key,
                                                type_desc text,
                                                price int,
                                                foreign key (id) references {SESSIONS} (type)
                                              )''')

            cur.execute(f'''create table if not exists {USERS} (
                                                            id serial primary key,
                                                            user_id int unique,
                                                            user_username text unique,
                                                            phone_number text,
                                                            foreign key (user_id) references {SESSIONS} (user_id),
                                                            foreign key (user_username) references {SESSIONS} (user_username)
                                                          )''')

            self.db_connection.commit()
            cur.close()
            logging.info(f"Database tables: «{SESSIONS}», «{TYPES}» and {USERS} created or verified.")

        except Exception as e:
            logging.error(f"Error initializing database: {e}.")

    def set_default_values(self):
        try:
            cur = self.get_connection().cursor()
            cur.execute(f'''insert into {TYPES}
                            select 1, "Drummer", 125
                            where
                                not exists (select 1 from {TYPES} where id = 1)
                            ''')

            cur.execute(f'''insert into {TYPES}
                            select 2, "Small band", 200
                            where
                                not exists (select 1 from {TYPES} where id = 2)
                            ''')
            cur.execute(f'''insert into {TYPES}
                            select 3, "Norm band", 300
                            where
                                not exists (select 1 from {TYPES} where id = 3)
                            ''')

            self.db_connection.commit()
            cur.close()
            logging.info(f"Table: «{TYPES}» set with default values.")

        except Exception as e:
            logging.error(f"Error setting default values in «{TYPES}»: {e}.")

    def close_database(self):
        if self.db_connection:
            try:
                self.db_connection.close()
                logging.info("Database connection closed.")
            except Exception as e:
                logging.error(f"Error closing database connection: {e}.")
        else:
            logging.warning("No open database connection to close or connection is already closed.")
