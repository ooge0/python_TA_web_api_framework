"""
General helper utilities.
"""
import os

from config.logger_config import get_logger


class GeneralUtils:
    """
    Small helpers:
    - write a list of test names to a file (used by the doc-inventory script)
    - string-to-boolean conversion
    """

    logger = get_logger()

    def create_file_and_write_test_names(self, test_list, file_path):
        """
        Write ``test_list`` to ``file_path``, one name per line, creating parent
        directories as needed.
        """
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as f:
                for test_name in test_list:
                    f.write(test_name + '\n')
            self.logger.info(f"Test names written to {file_path}")
        except Exception as e:
            self.logger.error(f"Error creating or writing to file: {e}")

    @staticmethod
    def str_to_bool(s: str) -> bool:
        """Return ``True`` for ``'true' / '1' / 't' / 'y' / 'yes'`` (any case)."""
        return s.lower() in ['true', '1', 't', 'y', 'yes']
