"""
Module for database management operations.
This module includes functions to create a SQLite database,
initialize tables, and populate them with test data.
"""
import os
import sqlite3

from utilities.db_utils import create_initial_test_data, connect_to_db
from utilities.general_utils import GeneralUtils
from utilities.read_configurations import read_configuration


def create_database(db_file):
    """Creates a SQLite database file.

    Args:
        db_file (str): The file path for the SQLite database.

    Returns:
        tuple: A connection and cursor object for the database.
    """
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    return conn, cursor


def create_tables(cursor):
    """Creates tables in the SQLite database.

    Args:
        cursor (sqlite3.Cursor): The cursor object used to execute SQL commands.
    """
    cursor.execute('''
      CREATE TABLE login_test_data (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          user_name TEXT,
          user_password TEXT
      )
  ''')

    cursor.execute('''
      CREATE TABLE booking_details (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT,
          email TEXT,
          phone TEXT,
          email_subject TEXT,
          contact_message_details TEXT
      )
  ''')

    cursor.execute('''
      CREATE TABLE user_details (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT,
          email TEXT,
          phone TEXT
      )
  ''')

    cursor.execute('''
      CREATE TABLE data_validation_admin_page_ui (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          valid_flag BOOL,
          admin_header_bar_room_title TEXT,
          admin_header_bar_report_title TEXT,
          admin_header_bar_branding_title TEXT,
          admin_header_bar_front_page_title TEXT,
          admin_header_bar_logout_title TEXT
      )
  ''')


def main():
    """Main function to set up the database and create initial tables."""
    db_file = read_configuration("db", "db_file")
    db_dir = read_configuration("db", "db_dir")

    print(f"db_file: '{db_file}'")  # Debugging output
    print(f"db_dir: '{db_dir}'")    # Debugging output

    full_path = GeneralUtils().get_path(db_dir, db_file)
    print(f"full_path: '{full_path}'")  # Debugging output
    connect_to_db(full_path)
    print(f"Current path for DB creations: {os.getcwd()}")
    conn, cursor = create_database(full_path)
    create_tables(cursor)
    conn.commit()
    create_initial_test_data(cursor)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    main()
