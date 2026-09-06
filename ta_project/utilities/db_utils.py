"""
Module defines several functions related to database operations, such as creating databases, connecting to them,
creating tables, and manipulating data.
It also makes logging actions of executed tasks.
"""
import os
import sqlite3
from collections import namedtuple

from config.logger_config import get_logger
from utilities.general_utils import GeneralUtils
from utilities.read_configurations import read_configuration
from utilities.test_data_utils import create_booking_details

logger = get_logger()


DBConfig = namedtuple('DBConfig', ['db_dir', 'db_file', 'db_full_path'])


def get_db_file_path_from_config():
    """
    Return the SQLite database location.

    ``TA_DB_PATH`` (set per-worker by the test session) wins over ``config.ini``,
    so ``pytest -n`` workers do not share one file.
    """
    env_path = os.environ.get("TA_DB_PATH")
    if env_path:
        return DBConfig(os.path.dirname(env_path), os.path.basename(env_path), os.path.abspath(env_path))
    db_file = read_configuration("db", "db_file")
    db_dir = read_configuration("db", "db_dir")
    return DBConfig(db_dir, db_file, GeneralUtils().get_path(db_dir, db_file))


def make_db():
    """
    Open (creating if needed) the SQLite database.

    Returns:
        tuple: ``(connection, cursor)``.
    """
    db_config = get_db_file_path_from_config()
    os.makedirs(os.path.dirname(db_config.db_full_path), exist_ok=True)
    existed = os.path.exists(db_config.db_full_path)
    conn = sqlite3.connect(db_config.db_full_path)
    logger.info(f"DB {'opened' if existed else 'created'}: {db_config.db_full_path}")
    return conn, conn.cursor()


def connect_to_db(db_file):
    """
    Connect to the SQLite database at ``db_file``.

    Returns:
        tuple: ``(connection, cursor)``.

    Raises:
        sqlite3.Error: on connection failure (previously this was swallowed and
            ``None`` was returned, so callers hit ``TypeError`` on unpack).
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn, conn.cursor()
    except sqlite3.Error as exc:
        logger.error(f"DB connection error for {db_file}: {exc}")
        raise


def create_database(db_file):
    """
    Creates a SQLite database file.

    Args:
        db_file (str): The path to the database file.

    Returns:
        tuple: A tuple containing the connection and cursor to the newly created database.
    """
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    return conn, cursor


def create_tables(cursor):
    """
    Creates necessary tables in the SQLite database.

    Args:
        cursor: The SQLite cursor used to execute SQL commands.
    """
    tables = [
        {
            "name": "login_test_data",
            "columns": [
                ("id", "INTEGER PRIMARY KEY AUTOINCREMENT"),
                ("user_name", "TEXT"),
                ("user_password", "TEXT")
            ]
        },
        {
            "name": "booking_details",
            "columns": [
                ("id", "INTEGER PRIMARY KEY AUTOINCREMENT"),
                ("name", "TEXT"),
                ("email", "TEXT"),
                ("phone", "TEXT"),
                ("email_subject", "TEXT"),
                ("contact_message_details", "TEXT")
            ]
        },
        {
            "name": "user_details",
            "columns": [
                ("id", "INTEGER PRIMARY KEY AUTOINCREMENT"),
                ("name", "TEXT"),
                ("email", "TEXT"),
                ("phone", "TEXT")
            ]
        },
        {
            "name": "data_validation_admin_page_ui",
            "columns": [
                ("id", "INTEGER PRIMARY KEY AUTOINCREMENT"),
                ("valid_flag", "BOOL"),
                ("admin_header_bar_room_title", "TEXT"),
                ("admin_header_bar_report_title", "TEXT"),
                ("admin_header_bar_branding_title", "TEXT"),
                ("branding_text_on_the_header_navbar", "TEXT"),
                ("admin_header_bar_front_page_title", "TEXT"),
                ("admin_header_bar_logout_title", "TEXT")
            ]
        }
    ]

    for table_data in tables:
        table_name = table_data["name"]
        columns = table_data["columns"]
        try:
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    {', '.join(f'{column[0]} {column[1]}' for column in columns)}
                )
            """)
            logger.info(f"Table '{table_name}' created successfully.")
        except sqlite3.Error as e:
            logger.info(f"Error creating table '{table_name}': {e}")


def get_data_from_db_as_dict(table_name):
    """
    Fetches data from a specified table in the SQLite database and returns it as a list of dictionaries.

    Args:
        table_name (str): The name of the table to fetch data from.

    Returns:
        list: A list of dictionaries representing the rows in the specified table.
    """
    db_dir, db_file, db_full_path = get_db_file_path_from_config()

    conn, cursor = connect_to_db(db_full_path)
    cursor.execute(f"SELECT * FROM {table_name}")
    columns = [col[0] for col in cursor.description]
    data = [dict(zip(columns, row)) for row in cursor.fetchall()]

    conn.close()
    return data


def create_initial_test_data(cursor):
    """
    Creates initial test data in the database, handling duplicates gracefully.

    Args:
        cursor: The SQLite cursor used to execute SQL commands.
    """
    details = create_booking_details("tests")
    name = details["name"]
    email = details["email"]
    phone = details["phone"]
    email_subject = details["email_subject"]
    contact_message_details = details["contact_message_details"]

    cursor.execute("SELECT id FROM user_details WHERE id = 1")
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO user_details (id, name, email, phone)
            VALUES (1, ?, ?, ?)
        """, (name, email, phone))
        logger.info("User record created in 'user_details' table.")

    cursor.execute("SELECT id FROM booking_details WHERE id = 1")
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO booking_details (id, name, email, phone, email_subject, contact_message_details)
            VALUES (1, ?, ?, ?, ?, ?)
        """, (name, email, phone, email_subject, contact_message_details))
        logger.info("Booking record created in 'booking_details' table.")

    cursor.execute("SELECT id FROM login_test_data WHERE id = 1")
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO login_test_data (id, user_name, user_password)
            VALUES (1, ?, ?)
        """, ('admin', 'password'))
        logger.info("Booking record created in 'login_test_data' table.")

    cursor.execute("SELECT id FROM data_validation_admin_page_ui WHERE id = 1")
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO data_validation_admin_page_ui (id, valid_flag, admin_header_bar_room_title, admin_header_bar_report_title,
             admin_header_bar_branding_title, branding_text_on_the_header_navbar, admin_header_bar_front_page_title, 
             admin_header_bar_logout_title)
            VALUES (1, ?, ?, ?, ?, ?, ?, ?)
        """, (True, 'Rooms', 'Report', 'Branding', 'B&B Booking Management', 'Front Page', 'Logout'))
        logger.info("Booking record created in 'data_validation_admin_page_ui' table.")


def drop_all_test_data(cursor):
    """
    Drops all test data tables from the database.

    Args:
        cursor: The SQLite cursor used to execute SQL commands.
    """
    cursor.execute("DROP TABLE IF EXISTS user_details")
    cursor.execute("DROP TABLE IF EXISTS booking_details")
    cursor.execute("DROP TABLE IF EXISTS login_test_data")
    cursor.execute("DROP TABLE IF EXISTS data_validation_admin_page_ui")
