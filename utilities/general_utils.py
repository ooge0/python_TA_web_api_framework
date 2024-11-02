"""
Utilities class provider
"""
import os
import sys
from typing import Optional

from config.logger_config import get_logger


def check_sys_env_issues():
    """
    Checks and logs system and environment details including:
    - Python system prefix
    - Current working directory
    - Environment variables

    Logs this information using the configured logger and also prints it to the console.
    """
    logger = get_logger()
    logger.debug(f"SYS.PREFIX: {sys.prefix}")
    logger.debug(f"OS.GETCWD(): {os.getcwd()}")
    logger.debug(f"OS.ENVIRON(): {os.environ}")

    print(f"SYS.PREFIX: {sys.prefix}")
    print(f"OS.GETCWD(): {os.getcwd()}")
    print(f"OS.ENVIRON(): {os.environ}")


class GeneralUtils:
    """
    A utility class providing helper methods for:
    - Taking screenshots in Selenium tests
    - Creating files and writing test names
    - Validating data retrieved from the database
    - Handling string-to-boolean conversions
    - Constructing normalized file paths
    """

    logger = get_logger()

    def take_screenshot(self, filename: Optional[str] = "page_screenshot.png"):
        """
        Takes a screenshot of the current web page in a Selenium test.

        Args:
            filename: Optional; The name of the screenshot file. Defaults to 'page_screenshot.png'.

        The screenshot is saved in the 'resources/screenshots/' directory. If the directory
        does not exist, it is created. The method logs the result and handles any errors.
        """
        screenshot_path = "resources/screenshots/"
        full_screenshot_path = os.path.join(screenshot_path, filename)
        try:
            os.makedirs(screenshot_path, exist_ok=True)  # Create directories if they don't exist
            self.driver.save_screenshot(full_screenshot_path)
            self.logger.info(f"Screenshot saved successfully as {full_screenshot_path}")
        except Exception as e:
            self.logger.error(f"Error saving screenshot: {e}")

    def create_file_and_write_test_names(self, test_list, file_path):
        """
        Creates a file and writes the list of test names to it, each on a new line.

        Args:
            test_list: A list of test names (strings) to be written into the file.
            file_path: The path where the file will be created. Directories in the path are
                       created if they do not exist.

        The method logs the operation and handles errors related to file creation or writing.
        """
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as f:
                for test_name in test_list:
                    f.write(test_name + '\n')
            self.logger.info(f"Test names written to {file_path}")
        except Exception as e:
            self.logger.error(f"Error creating or writing to file: {e}")

    def get_validation_data_from_db(self, data, key):
        """
        Validates and retrieves data from a database response.

        Args:
            data: A list of dictionary objects returned from the database.
            key: The key whose corresponding value needs to be retrieved from the data.

        Returns:
            The value from the database data corresponding to the provided key.

        If the key is not found, an error is logged. This method assumes the data is
        structured as a list of dictionaries and attempts to retrieve data from the first
        dictionary.
        """
        try:
            data = data[0][key]
            self.logger.debug(f"Retrieved from DB: {data} by key {key}")
        except KeyError as e:
            self.logger.error(f"Error. Check DB table or related enum class for missing key {key}")
        return data

    @staticmethod
    def str_to_bool(s: str) -> bool:
        """
        Converts a string to a boolean value.

        Args:
            s: The string to be converted.

        Returns:
            True if the string represents a truthy value ('true', '1', 't', 'y', 'yes'),
            otherwise False.
        """
        return s.lower() in ['true', '1', 't', 'y', 'yes']

    @staticmethod
    def get_path(db_dir: str, db_file: str) -> str:
        """
        Constructs a normalized file path from a project root, directory, and file name.

        Args:
            db_dir: The directory path (may include unwanted leading/trailing characters).
            db_file: The database file name.

        Returns:
            A normalized full file path constructed from the project root, the cleaned
            directory path, and the database file name.
        """
        # Get the root of the project by moving up from the current file's directory
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Normalize db_dir to remove any unwanted characters or leading/trailing spaces
        db_dir = db_dir.strip().lstrip('=').strip()  # Removes leading '=' and whitespace

        # Construct the full path from the project root
        full_path = os.path.join(project_root, db_dir, db_file)

        # Normalize the path to ensure it's well-formed
        full_path = os.path.normpath(full_path)

        return full_path
