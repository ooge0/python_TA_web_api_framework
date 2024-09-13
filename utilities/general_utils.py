import os
import sys
from typing import Optional

from config.logger_config import get_logger


def check_sys_env_issues():
    logger = get_logger()
    logger.debug(f"SYS.PREFIX:{sys.prefix}")
    logger.debug(f"OS.GETCWD():{os.getcwd()}")
    logger.debug(f"OS.ENVIRON():{os.environ}")

    print(f"SYS.PREFIX:{sys.prefix}")
    print(f"OS.GETCWD():{os.getcwd()}")
    print(f"OS.ENVIRON():{os.environ}")


class GeneralUtils:
    logger = get_logger()

    def take_screenshot(self, filename: Optional[str] = "page_screenshot.png"):
        screenshot_path = f"resources/screenshots/"
        full_screenshot_path = os.path.join(screenshot_path, filename)
        try:
            os.makedirs(screenshot_path, exist_ok=True)  # Create directories if they don't exist
            self.driver.save_screenshot(full_screenshot_path)
            self.logger.info(f"Screenshot saved successfully as {full_screenshot_path}")
        except Exception as e:
            self.logger.error(f"Error saving screenshot: {e}")

    def create_file_and_write_test_names(self, test_list, file_path):
        """
        Creates a file and writes tests names to it.

        Args:
            test_list: A list of tests names.
            file_path: The path to the file to create.
        """

        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as f:
                for test_name in test_list:
                    f.write(test_name + '\n')
        except Exception as e:
            self.logger.error(f"Error creating or writing to file: {e}")

    def get_validation_data_from_db(self, data, key):
        try:
            data = data[0][key]
            self.logger.debug(f"Retrieved from db data: {data}, by key{key}")
        except KeyError as e:
            self.logger.error(f"Error. Check DB table or related to the actions the enum class")
        return data



    @staticmethod
    def str_to_bool(s):
        """
        Define simple replacement of bool values via aliases
        :param s:
        :return:
        """
        return s.lower() in ['true', '1', 't', 'y', 'yes']

    @staticmethod
    def get_path(db_dir: str, db_file: str):
        # Get the root of the project by moving up from the current file's directory
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Normalize db_dir to remove any unwanted characters or leading/trailing spaces
        db_dir = db_dir.strip().lstrip('=').strip()  # Removes leading '=' and whitespace

        # Construct the full path from the project root
        full_path = os.path.join(project_root, db_dir, db_file)

        # Normalize the path to ensure it's well-formed
        full_path = os.path.normpath(full_path)

        return full_path
