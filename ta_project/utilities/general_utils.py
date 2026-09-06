"""
General helper utilities.
"""
import os

from config.logger_config import get_logger


class GeneralUtils:
    """
    Helper methods for:
    - Creating files and writing test names
    - Reading a value out of a database result
    - String-to-boolean conversion
    - Building a normalised path under the project root
    """

    logger = get_logger()

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
        Retrieve ``data[0][key]`` from a database result.

        Args:
            data: A list of dictionary objects returned from the database.
            key: The key whose value to retrieve from the first row.

        Returns:
            The value from the first row for the given key.

        Raises:
            KeyError: if the key is not present in the first row (previously this
                was swallowed and the whole input list was returned instead,
                which silently broke the caller's assertions).
        """
        try:
            value = data[0][key]
        except (KeyError, IndexError):
            self.logger.error(f"Missing key '{key}' in DB row - check the table or the related enum class")
            raise
        self.logger.debug(f"Retrieved from DB: {value} by key {key}")
        return value

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
