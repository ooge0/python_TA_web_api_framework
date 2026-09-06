# /core/data/data_factory/data_factory.py
"""
Package contains methods for extracting test data as data sets
from different sources like  Excel files, fixtures, external DBs.
Package contains methods get data using 'valid_data_flag' that will reference to set
of valid/invalid data for tests.
"""
from typing import List, Optional

from config.logger_config import get_logger
from core.data.data_models.api_login_data_models import LoginCredentials
from utilities.excel_data_provider import ExcelDataProvider


class DataFactory:
    """
    Class for manipulating data from external sources as test data
    """
    def __init__(self, file_path: str):
        self.provider = ExcelDataProvider(file_path)
        self.logger = get_logger()

    def create_login_test_data(self, sheet_name: str, valid_data_flag: bool,
                               excel_test_data_index: Optional[int] = None) -> List[LoginCredentials]:
        """
        Method creates data that is retried from Excel file

        :param sheet_name:
        :param valid_data_flag: Used for getting data for positive tests(flag=1) and negative if flag=0
        :param excel_test_data_index:

        :return: Login credentials: user_name, user_password,
        """
        raw_data = self.provider.get_valid_data(sheet_name) if valid_data_flag else self.provider.get_invalid_data(sheet_name)
        if excel_test_data_index is not None:
            if excel_test_data_index == 'all':
                data = [
                    LoginCredentials(user_name, user_password, valid=valid_data_flag)
                    for user_name, user_password in raw_data
                ]
            else:
                try:
                    user_name, user_password = self.provider.get_data_by_index(raw_data, excel_test_data_index)
                    data = [LoginCredentials(user_name, user_password, valid=valid_data_flag)]
                except IndexError:
                    self.logger.error(f"Index {excel_test_data_index} is out of range for data in {sheet_name}.")
                    raise ValueError(f"Index {excel_test_data_index} is out of range for data in {sheet_name}.")
        else:
            data = [LoginCredentials(user_name, user_password, valid=valid_data_flag) for user_name, user_password in raw_data]
        self.logger.info(f"Login test data: {data}")
        return data
