import os
import sqlite3
from collections import namedtuple

from config.logger_config import get_logger
from utilities.general_utils import GeneralUtils
from utilities.read_configurations import read_configuration
from utilities.test_data_utils import create_booking_details

logger = get_logger()


def get_db_file_path_from_config():
    db_file = read_configuration("db", "db_file")
    db_dir = read_configuration("db", "db_dir")
    db_full_path = GeneralUtils().get_path(db_dir, db_file)
    DBConfig = namedtuple('DBConfig', ['db_dir', 'db_file', 'db_full_path'])
    return DBConfig(db_dir, db_file, db_full_path)


def make_db():
    """Creates a SQLite database file if it doesn't exist."""
    db_config = get_db_file_path_from_config()

    os.makedirs(os.path.dirname(db_config.db_full_path), exist_ok=True)

    # Check if the database file exists
    if not os.path.exists(db_config.db_full_path):
        # Create the database file
        conn = sqlite3.connect(db_config.db_full_path)
        cursor = conn.cursor()
        logger.info(f"DB created. Used configuration: db_dir: {db_config.db_dir}, db_file: {db_config.db_file}")
        return conn, cursor
    else:
        # Connect to the existing database
        conn = sqlite3.connect(db_config.db_full_path)
        cursor = conn.cursor()
        logger.info(
            f"DB already created. Used configuration:  db_dir: {db_config.db_dir}, db_file: {db_config.db_file}")
        return conn, cursor


def connect_to_db(db_file):
    """Connect to DB"""
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        return conn, cursor
    except sqlite3.Error as e:
        logger.error(f"DB connection error: {e}")


def create_database(db_file):
    """Creates a SQLite database file."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    return conn, cursor


def create_tables(cursor):
    """Creates tables in the database."""

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
    db_dir, db_file, db_full_path = get_db_file_path_from_config()

    """Fetches data from a SQLite database and returns it as a list of dictionaries."""
    conn, cursor = connect_to_db(db_full_path)
    cursor.execute(f"SELECT * FROM {table_name}")
    columns = [col[0] for col in cursor.description]
    data = [dict(zip(columns, row)) for row in cursor.fetchall()]

    conn.close()
    return data


def create_initial_test_data(cursor):
    """
    Creates initial test data in the database, handling duplicates gracefully.
    """
    name, email, phone, email_subject, contact_message_details = create_booking_details("tests")

    # Check for existing user in 'user_details'
    cursor.execute("SELECT id FROM user_details WHERE id = 1")
    if not cursor.fetchone():  # If user doesn't exist
        cursor.execute("""
            INSERT INTO user_details (id, name, email, phone)
            VALUES (1, ?, ?, ?)
        """, (name, email, phone))
        logger.info("User record created in 'user_details' table.")

    # Check for existing booking in 'booking_details'
    cursor.execute("SELECT id FROM booking_details WHERE id = 1")
    if not cursor.fetchone():  # If booking_details doesn't exist
        cursor.execute("""
            INSERT INTO booking_details (id, name, email, phone, email_subject, contact_message_details)
            VALUES (1, ?, ?, ?, ?, ?)
        """, (name, email, phone, email_subject, contact_message_details))
        logger.info("Booking record created in 'booking_details' table.")

    # Check for existing booking in 'login_test_data'
    cursor.execute("SELECT id FROM login_test_data WHERE id = 1")
    if not cursor.fetchone():  # If login_test_data doesn't exist
        cursor.execute("""
            INSERT INTO login_test_data (id, user_name, user_password)
            VALUES (1, ?, ?)
        """, ('admin', 'password'))
        logger.info("Booking record created in 'login_test_data' table.")

    # Check for existing booking in 'data_validation_admin_page_ui'
    cursor.execute("SELECT id FROM data_validation_admin_page_ui WHERE id = 1")
    if not cursor.fetchone():  # If data_validation_admin_page_ui doesn't exist
        cursor.execute("""
            INSERT INTO data_validation_admin_page_ui (id, valid_flag, admin_header_bar_room_title, admin_header_bar_report_title,
             admin_header_bar_branding_title, branding_text_on_the_header_navbar, admin_header_bar_front_page_title, 
             admin_header_bar_logout_title)
        VALUES (1, ?, ?, ?, ?, ?, ?, ?)
        """, (True, 'Rooms', 'Report', 'Branding', 'B&B Booking Management', 'Front Page', 'Logout'))
        logger.info("Booking record created in 'data_validation_admin_page_ui' table.")


def drop_all_test_data(cursor):
    """
    Drops all test data tables.
    """
    cursor.execute("DROP TABLE IF EXISTS user_details")
    cursor.execute("DROP TABLE IF EXISTS booking_details")
    cursor.execute("DROP TABLE IF EXISTS login_test_data")
    cursor.execute("DROP TABLE IF EXISTS data_validation_admin_page_ui")
