# /utilities/excel_data_provider.py

"""
Module for providing data from Excel files.
This module includes the ExcelDataProvider class, which offers methods to
retrieve user credentials from an Excel sheet, both valid and invalid,
and supports data retrieval by index.
"""

from typing import List, Tuple

import openpyxl

from config.logger_config import get_logger


class ExcelDataProvider:
    """Class to handle data extraction from an Excel file."""

    def __init__(self, file_path: str):
        """Initializes the ExcelDataProvider with the given file path.

        Args:
            file_path (str): The path to the Excel file from which to retrieve data.
        """
        self.file_path = file_path
        self.logger = get_logger()

    def get_data(self, sheet_name: str, flag: bool) -> List[Tuple[str, str]]:
        """
        Extracts a set of user credentials from the specified Excel sheet.

        Args:
            sheet_name (str): The name of the sheet to retrieve data from.
            flag (bool): Indicates whether to extract positive (True) or negative (False) test data.

        Returns:
            List[Tuple[str, str]]: Retrieved test data, where each tuple contains user_name and user_password.
        """
        workbook = openpyxl.load_workbook(self.file_path)
        sheet = workbook[sheet_name]
        data = []
        for row in sheet.iter_rows(min_row=2, values_only=True):
            if row[0] == flag:
                data.append((row[1], row[2]))  # user_name and user_password are in the second and third columns
        self.logger.info(f"Retrieved test data from Excel file: {data}")
        return data

    def get_valid_data(self, sheet_name: str) -> List[Tuple[str, str]]:
        """
        Retrieves valid test data from the specified Excel sheet.

        Args:
            sheet_name (str): The name of the sheet to retrieve valid data from.

        Returns:
            List[Tuple[str, str]]: Retrieved valid test data.
        """
        return self.get_data(sheet_name, True)

    def get_invalid_data(self, sheet_name: str) -> List[Tuple[str, str]]:
        """
        Retrieves invalid test data from the specified Excel sheet.

        Args:
            sheet_name (str): The name of the sheet to retrieve invalid data from.

        Returns:
            List[Tuple[str, str]]: Retrieved invalid test data.
        """
        return self.get_data(sheet_name, False)

    def get_data_by_index(self, data: List[Tuple[str, str]], index: int) -> Tuple[str, str]:
        """
        Retrieves data from the provided list by index.

        Args:
            data (List[Tuple[str, str]]): The list of data from which to retrieve a tuple.
            index (int): The index of the data to retrieve.

        Returns:
            Tuple[str, str]: The retrieved tuple of data.

        Raises:
            IndexError: If the index is out of range of the data list.
        """
        if 0 <= index < len(data):
            return data[index]
        else:
            raise IndexError("Data index out of range")
