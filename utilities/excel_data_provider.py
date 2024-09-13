# excel_data_provider.py
from typing import List, Tuple

import openpyxl

from config.logger_config import get_logger


class ExcelDataProvider:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.logger = get_logger()

    def get_data(self, sheet_name: str, flag: bool) -> List[Tuple[str, str]]:
        """
        Method extract positive/negative set of test data for next usage from Excel doc.

        :param sheet_name:
        :param flag: It's using for checking relations of extracted test data from
        Excel doc tab (the first column).
        :return:
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
        return self.get_data(sheet_name, True)

    def get_invalid_data(self, sheet_name: str) -> List[Tuple[str, str]]:
        return self.get_data(sheet_name, False)

    def get_data_by_index(self, data: List[Tuple[str, str]], index: int) -> Tuple[str, str]:
        if 0 <= index < len(data):
            return data[index]
        else:
            raise IndexError("Data index out of range")
