import sqlite3
import logging
from logger.logger import setup_logger

# from config_data.config import load_config

DATABASE_FILE = 'database/garage.db'
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

            self.db_connection.commit()
            cur.close()
            logging.info(f"Database tables: «{SESSIONS}», «{TYPES}» created or verified.")

        except Exception as e:
            logging.error(f"Error initializing database: {e}.")

    def set_default_values(self):
        try:
            cur = self.get_connection().cursor()
            cur.execute(f'''insert into {TYPES}
                            select 1, "Drummer", 150
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

    def sessions_random_data(self):
        try:
            cur = self.get_connection().cursor()
            cur.execute(f"""INSERT INTO {SESSIONS} (user_id, user_username, session_start, session_end, duration, type)
                            VALUES
                                (288878378, 'georgenegeorge', '2024-04-03 15:00:00', '2024-04-03 18:00:00', 3, 1),
                                (288878378, 'georgenegeorge', '2024-04-03 19:00:00', '2024-04-03 20:00:00', 1, 2),
                                (288878378, 'georgenegeorge', '2024-04-03 09:00:00', '2024-04-03 11:00:00', 2, 1),
                                (288878378, 'georgenegeorge', '2024-04-03 11:00:00', '2024-04-03 14:00:00', 3, 3),
                                (288878378, 'georgenegeorge', '2024-04-03 23:00:00', '2024-04-05 02:00:00', 3, 3);
                                """)
            self.db_connection.commit()
            cur.close()
            logging.info(f"Table: «{SESSIONS}» set with test values.")

        except Exception as e:
            logging.error(f"Error setting default values in «{SESSIONS}»: {e}.")

    def close_database(self):
        if self.db_connection:
            try:
                self.db_connection.close()
                logging.info("Database connection closed.")
            except Exception as e:
                logging.error(f"Error closing database connection: {e}.")
        else:
            logging.warning("No open database connection to close or connection is already closed.")


db_manager = Database()
conn = db_manager.get_connection()
db_manager.get_connection()
# db_manager.create_tables()
# db_manager.set_default_values()
# db_manager.sessions_random_data()
cur = conn.cursor()
cur.execute(f'select * from {SESSIONS}')
column_names = [column[0] for column in cur.description]
print(' '.join(name.ljust(20) for name in column_names))
for row in cur:
    print(' '.join(str(item).ljust(20) for item in row))
cur.close()
