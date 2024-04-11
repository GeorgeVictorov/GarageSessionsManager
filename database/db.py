import psycopg
import logging
from cachetools import cached, TTLCache
from config_data.config import load_config

SESSIONS = 'garage_sessions'
TYPES = 'session_types'
USERS = 'garage_users'
PAYMENTS = 'sessions_payment'

cache = TTLCache(maxsize=100, ttl=300)


def update_cached_users():
    cache.clear()
    logging.info("Cached users cleared.")


class Database:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.config = load_config()
            self.db_connection = None
            self._initialize_connection()
            self._initialized = True

    def _initialize_connection(self):
        if self.db_connection is None:
            try:
                logging.info("Creating a new database connection...")
                self.db_connection = psycopg.connect(
                    dbname=self.config.db.database,
                    user=self.config.db.db_user,
                    password=self.config.db.db_password,
                    host=self.config.db.db_host
                )
                logging.info("Database connection created successfully.")
            except psycopg.Error as e:
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
                cur.execute(f'''create table if not exists {TYPES} (
                                    id serial primary key,
                                    type_desc text,
                                    price int
                                              )''')

                cur.execute(f'''create table if not exists {USERS} (
                                    id serial primary key,
                                    user_id bigint unique,
                                    user_username text unique,
                                    phone_number text,
                                    is_banned boolean default false
                                                          )''')

                cur.execute(f'''create table if not exists {SESSIONS} (
                                    id serial primary key,
                                    user_id bigint,
                                    user_username text,
                                    session_start timestamp,
                                    session_end timestamp,
                                    duration int,
                                    type int,
                                    is_payed boolean default false,
                                    is_canceled boolean default false,
                                    foreign key (type) references {TYPES} (id),
                                    foreign key (user_id) references {USERS} (user_id),
                                    foreign key (user_username) references {USERS} (user_username)
                                                              )''')

                cur.execute(f'''create table if not exists {PAYMENTS} (
                                    payment_id serial primary key,
                                    session_id int unique,
                                    total_price int,
                                    payed_on date default current_date,
                                    foreign key (session_id) references {SESSIONS} (id)
                                                                      )''')

                self.db_connection.commit()
            logging.info(f"Database tables: «{SESSIONS}», «{TYPES}», «{USERS}» and «{PAYMENTS}» created or verified.")

        except Exception as e:
            logging.error(f"Error initializing database: {e}.")

    def set_default_values(self):
        try:
            with self.get_connection().cursor() as cursor:
                cursor.execute(f'''insert into {TYPES}
                                select 1, 'Drummer', 125
                                where
                                    not exists (select 1 from {TYPES} where id = 1)
                            ''')

                cursor.execute(f'''insert into {TYPES}
                                select 2, 'Small band', 200
                                where
                                    not exists (select 1 from {TYPES} where id = 2)
                            ''')

                cursor.execute(f'''insert into {TYPES}
                                select 3, 'Norm band', 300
                                where
                                    not exists (select 1 from {TYPES} where id = 3)
                            ''')

                self.db_connection.commit()
            logging.info(f"Table: «{TYPES}» set with default values.")

        except Exception as e:
            logging.error(f"Error setting default values in «{TYPES}»: {e}.")

    @cached(cache=cache)
    def check_user_registration(self, user_id):
        try:
            with self.get_connection().cursor() as cursor:
                cursor.execute(f'select 1 from {USERS} where user_id = %s and is_banned = false', (user_id,))
                is_registered = cursor.fetchone()
                logging.info(f'Retrieved check_user_registration data.')
                return is_registered
        except Exception as e:
            logging.error(f"Error getting data from «{USERS}»: {e}.")

    def add_user(self, user_id: int, username: str, phone_number: str):
        try:
            with self.get_connection().cursor() as cursor:
                cursor.execute(f'''insert into {USERS} (user_id, user_username, phone_number)
                                values (%s, %s, %s)''', (user_id, username, phone_number))
                self.db_connection.commit()
            logging.info(f'New user: {username} added to {USERS} table.')
        except Exception as e:
            logging.error(f"Error adding new user: {username} to «{USERS}»: {e}.")

    def close_database(self):
        if self.db_connection:
            try:
                self.db_connection.close()
                logging.info("Database connection closed.")
            except Exception as e:
                logging.error(f"Error closing database connection: {e}.")
        else:
            logging.warning("No open database connection to close or connection is already closed.")
